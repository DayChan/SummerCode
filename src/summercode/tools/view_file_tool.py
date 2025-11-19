import os
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class ViewFileToolInput(BaseModel):
    file_path: str = Field(..., description="The absolute path to the file to view.")
    start_line: Optional[int] = Field(None, description="The starting line number (1-indexed).")
    end_line: Optional[int] = Field(None, description="The ending line number (1-indexed).")

class ViewFileTool(BaseTool):
    name: str = "view_file_tool"
    description: str = "View the contents of a file."
    args_schema: Type[BaseModel] = ViewFileToolInput

    def _run(
        self, 
        file_path: str, 
        start_line: Optional[int] = None, 
        end_line: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            if not os.path.exists(file_path):
                return f"Error: File {file_path} does not exist."
                
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
                
            total_lines = len(lines)
            
            if start_line is None:
                start_line = 1
            if end_line is None:
                end_line = total_lines
                
            if start_line < 1:
                start_line = 1
            if end_line > total_lines:
                end_line = total_lines
                
            if start_line > end_line:
                return f"Error: Start line {start_line} is greater than end line {end_line}."

            # Adjust for 0-based indexing
            selected_lines = lines[start_line-1:end_line]
            
            content = "".join(selected_lines)
            return f"File: {file_path}\nLines {start_line}-{end_line} of {total_lines}:\n\n{content}"
            
        except Exception as e:
            return f"Error viewing file: {e}"
