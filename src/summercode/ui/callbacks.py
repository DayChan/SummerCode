from typing import Any, Dict, List, Optional
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from textual.widgets import RichLog
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

class TextualCallbackHandler(BaseCallbackHandler):
    """Callback Handler that writes to a Textual RichLog widget."""

    def __init__(self, rich_log: RichLog, on_token_usage: Optional[callable] = None):
        self.rich_log = rich_log
        self.on_token_usage = on_token_usage

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        self.rich_log.write(Panel(Text("Thinking...", style="bold yellow"), title="LLM Start"))

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        if self.on_token_usage and response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})
            total_tokens = token_usage.get("total_tokens", 0)
            if total_tokens > 0:
                self.on_token_usage(total_tokens)

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Run when tool starts running."""
        tool_name = serialized.get("name")
        self.rich_log.write(Panel(Text(f"Executing tool: {tool_name}\nInput: {input_str}", style="bold cyan"), title="Tool Start"))

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Run when tool ends running."""
        # self.rich_log.write(Panel(Text(f"Tool Output:\n{output}", style="dim"), title="Tool End"))
        pass

    def on_agent_action(self, action: Any, **kwargs: Any) -> Any:
        """Run on agent action."""
        self.rich_log.write(Panel(Text(f"Agent Action: {action.tool}\nInput: {action.tool_input}", style="bold blue"), title="Agent Action"))

    def on_agent_finish(self, finish: Any, **kwargs: Any) -> None:
        """Run on agent end."""
        output = finish.return_values.get("output")
        self.rich_log.write(Panel(Markdown(output), title="Agent Finish", style="bold green"))

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        # For now, we might not need this if we are not streaming to the log directly in real-time for tokens
        pass
