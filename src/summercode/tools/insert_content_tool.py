import os
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class InsertContentToolInput(BaseModel):
    file_path: str = Field(..., description="The absolute path to the file.")
    content: str = Field(..., description="The content to insert.")
    line_number: int = Field(..., description="The line number to insert at (1-indexed). Content will be inserted BEFORE this line.")

class InsertContentTool(BaseTool):
    name: str = "insert_content_tool"
    description: str = "Insert content into a file at a specific line."
    args_schema: Type[BaseModel] = InsertContentToolInput

    def _run(
        self, 
        file_path: str, 
        content: str, 
        line_number: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            if not os.path.exists(file_path):
                return f"Error: File {file_path} does not exist."
                
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if line_number < 1:
                line_number = 1
            
            # If line_number is greater than file length + 1, just append
            if line_number > len(lines) + 1:
                line_number = len(lines) + 1
                
            # Insert content
            # Ensure content ends with newline if it's a separate block
            if not content.endswith('\n'):
                content += '\n'
                
            lines.insert(line_number - 1, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
                
            return f"Successfully inserted content at line {line_number} in {file_path}"
        except Exception as e:
            return f"Error inserting content: {e}"
