import os
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class CreateFileToolInput(BaseModel):
    file_path: str = Field(..., description="The absolute path to the file to create.")
    content: str = Field(..., description="The content to write to the file.")
    overwrite: bool = Field(False, description="Whether to overwrite if the file exists.")

class CreateFileTool(BaseTool):
    name: str = "create_file_tool"
    description: str = "Create a new file with specified content."
    args_schema: Type[BaseModel] = CreateFileToolInput

    def _run(
        self, 
        file_path: str, 
        content: str, 
        overwrite: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            if os.path.exists(file_path) and not overwrite:
                return f"Error: File {file_path} already exists. Set overwrite=True to overwrite."
            
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return f"Successfully created file {file_path}"
        except Exception as e:
            return f"Error creating file: {e}"
