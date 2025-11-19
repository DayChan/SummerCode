import os
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class StrReplaceToolInput(BaseModel):
    file_path: str = Field(..., description="The absolute path to the file.")
    old_str: str = Field(..., description="The string to replace.")
    new_str: str = Field(..., description="The replacement string.")

class StrReplaceTool(BaseTool):
    name: str = "str_replace_tool"
    description: str = "Replace all occurrences of a string in a file."
    args_schema: Type[BaseModel] = StrReplaceToolInput

    def _run(
        self, 
        file_path: str, 
        old_str: str, 
        new_str: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            if not os.path.exists(file_path):
                return f"Error: File {file_path} does not exist."
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if old_str not in content:
                return f"Warning: String '{old_str}' not found in {file_path}."
                
            new_content = content.replace(old_str, new_str)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            return f"Successfully replaced occurrences of '{old_str}' with '{new_str}' in {file_path}"
        except Exception as e:
            return f"Error replacing string: {e}"
