import os
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class TreeToolInput(BaseModel):
    directory_path: Optional[str] = Field(
        default=".", 
        description="The path to the directory to show tree structure for. Defaults to current directory."
    )
    max_depth: Optional[int] = Field(
        default=3,
        description="The maximum depth to traverse. Defaults to 3."
    )

class TreeTool(BaseTool):
    name: str = "tree_tool"
    description: str = "Show the file system structure of a directory in a tree-like format."
    args_schema: Type[BaseModel] = TreeToolInput

    def _run(
        self, 
        directory_path: str = ".", 
        max_depth: int = 3,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            tree_str = ""
            start_path = directory_path
            
            for root, dirs, files in os.walk(start_path):
                level = root.replace(start_path, '').count(os.sep)
                if level > max_depth:
                    continue
                    
                indent = ' ' * 4 * (level)
                tree_str += f"{indent}{os.path.basename(root)}/\n"
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    tree_str += f"{subindent}{f}\n"
            
            return tree_str
        except Exception as e:
            return f"Error generating tree: {e}"
