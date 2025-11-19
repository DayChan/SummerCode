import os
import re
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class GrepToolInput(BaseModel):
    pattern: str = Field(..., description="The regular expression pattern to search for.")
    directory_path: Optional[str] = Field(
        default=".", 
        description="The path to the directory to search in. Defaults to current directory."
    )
    recursive: Optional[bool] = Field(
        default=True,
        description="Whether to search recursively. Defaults to True."
    )

class GrepTool(BaseTool):
    name: str = "grep_tool"
    description: str = "Search for a pattern in files within a directory."
    args_schema: Type[BaseModel] = GrepToolInput

    def _run(
        self, 
        pattern: str, 
        directory_path: str = ".", 
        recursive: bool = True,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        results = []
        try:
            regex = re.compile(pattern)
            
            if recursive:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self._search_file(file_path, regex, results)
            else:
                if os.path.isdir(directory_path):
                    for file in os.listdir(directory_path):
                        file_path = os.path.join(directory_path, file)
                        if os.path.isfile(file_path):
                            self._search_file(file_path, regex, results)
                elif os.path.isfile(directory_path):
                     self._search_file(directory_path, regex, results)

            return "\n".join(results) if results else "No matches found."
        except Exception as e:
            return f"Error grepping: {e}"

    def _search_file(self, file_path, regex, results):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if regex.search(line):
                        results.append(f"{file_path}:{i+1}: {line.strip()}")
        except Exception:
            pass # Ignore files that cannot be read
