import subprocess
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class BashToolInput(BaseModel):
    command: str = Field(..., description="The bash command to execute.")

class BashTool(BaseTool):
    name: str = "bash_tool"
    description: str = "Execute a bash command."
    args_schema: Type[BaseModel] = BashToolInput

    def _run(
        self, 
        command: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        if "rm " in command or command.strip() == "rm":
            return "Command blocked: 'rm' is not allowed for safety reasons."
            
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=10
            )
            output = result.stdout
            if result.stderr:
                output += f"\nStderr: {result.stderr}"
            return output if output else "Command executed successfully with no output."
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 10 seconds."
        except Exception as e:
            return f"Error executing command: {e}"
