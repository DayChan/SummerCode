import asyncio
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, RichLog, Static
from textual.worker import Worker, WorkerState

from summercode.models.chat_model import init_chat_model
from summercode.agents.coding_agent import create_coding_agent
from summercode.ui.callbacks import TextualCallbackHandler

class SummerCodeApp(App):
    """A Textual app for the SummerCode Coding Agent."""

    CSS = """
    Screen {
        layout: vertical;
    }

    #chat-container {
        height: 1fr;
        border: solid green;
        margin: 1;
    }

    RichLog {
        height: 1fr;
        overflow-y: scroll;
    }

    Input {
        dock: bottom;
        margin: 1;
    }

    #token_stats {
        dock: top;
        height: 1;
        background: $primary;
        color: $text;
        padding: 0 1;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Total Tokens: 0", id="token_stats")
        with Container(id="chat-container"):
            yield RichLog(id="chat_log", highlight=True, markup=True)
        yield Input(placeholder="Type your instruction here...", id="user_input")
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.chat_log = self.query_one(RichLog)
        self.user_input = self.query_one(Input)
        self.user_input.focus()
        
        # Initialize agent
        self.llm = init_chat_model()
        self.agent = create_coding_agent(self.llm)
        self.total_tokens = 0
        
        self.chat_log.write("[bold green]Welcome to SummerCode Agent![/bold green]")

    def update_token_count(self, tokens: int) -> None:
        """Update the total token count."""
        self.total_tokens += tokens
        self.query_one("#token_stats", Static).update(f"Total Tokens: {self.total_tokens}")

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle user input submission."""
        user_message = message.value
        if not user_message:
            return

        self.user_input.value = ""
        self.chat_log.write(f"[bold magenta]User:[/bold magenta] {user_message}")
        
        # Run agent in a worker to avoid blocking the UI
        self.run_agent(user_message)

    @work(exclusive=True)
    async def run_agent(self, user_message: str) -> None:
        """Run the agent in a background worker."""
        callback = TextualCallbackHandler(
            self.chat_log, 
            on_token_usage=lambda tokens: self.call_from_thread(self.update_token_count, tokens)
        )
        try:
            # Since invoke is synchronous, we might need to run it in a thread if we want to be truly async, 
            # but Textual's worker can handle it. However, langchain invoke is blocking.
            # Better to use a thread worker.
            await asyncio.to_thread(self._run_agent_sync, user_message, callback)
        except Exception as e:
            self.chat_log.write(f"[bold red]Error:[/bold red] {str(e)}")

    def _run_agent_sync(self, user_message: str, callback: TextualCallbackHandler) -> None:
        result = self.agent.invoke(
            {"messages": [("user", user_message)]},
            config={"callbacks": [callback]}
        )
        # The result should contain the final response
        if "messages" in result and len(result["messages"]) > 0:
            final_message = result["messages"][-1]
            if hasattr(final_message, 'content'):
                self.chat_log.write(f"[bold green]Agent:[/bold green] {final_message.content}")

if __name__ == "__main__":
    app = SummerCodeApp()
    app.run()
