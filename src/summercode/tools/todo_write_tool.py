import os
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class TodoWriteToolInput(BaseModel):
    todo_item: str = Field(..., description="The TODO item to add.")
    file_path: Optional[str] = Field(
        default="TODO.md", 
        description="The path to the TODO file. Defaults to TODO.md."
    )

class TodoWriteTool(BaseTool):
    name: str = "todo_write_tool"
    description: str = "Append a TODO item to a file."
    args_schema: Type[BaseModel] = TodoWriteToolInput

    def _run(
        self, 
        todo_item: str, 
        file_path: str = "TODO.md", 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            # Ensure directory exists if path contains one
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"- [ ] {todo_item}\n")
            return f"Added TODO item to {file_path}"
        except Exception as e:
            return f"Error writing TODO: {e}"
