import os
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class ListDirectoryInput(BaseModel):
    directory_path: Optional[str] = Field(
        default=".", 
        description="The path to the directory to list. Defaults to current directory."
    )

class ListDirectoryTool(BaseTool):
    name: str = "ls_tool"
    description: str = "List files and directories in a given path."
    args_schema: Type[BaseModel] = ListDirectoryInput

    def _run(
        self, 
        directory_path: str = ".", 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            files = os.listdir(directory_path)
            return "\n".join(files)
        except Exception as e:
            return f"Error listing directory: {e}"
