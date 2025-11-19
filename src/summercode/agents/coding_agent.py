from langchain.agents import create_agent
from summercode.tools import (
    ListDirectoryTool, 
    TreeTool, 
    GrepTool, 
    BashTool, 
    TodoWriteTool,
    ViewFileTool,
    CreateFileTool,
    InsertContentTool,
    StrReplaceTool
)

def create_coding_agent(llm):
    """
    Create a coding agent with access to file system and bash tools.
    
    Args:
        llm: The language model to use.
        
    Returns:
        The created agent graph.
    """
    tools = [
        ListDirectoryTool(),
        TreeTool(),
        GrepTool(),
        BashTool(),
        TodoWriteTool(),
        ViewFileTool(),
        CreateFileTool(),
        InsertContentTool(),
        StrReplaceTool()
    ]
    
    system_prompt = "You are a helpful coding assistant. You have access to the file system and can execute bash commands."
    
    agent = create_agent(llm, tools, system_prompt=system_prompt)
    return agent