"""
Test script for all SummerCode tools.
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

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

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def test_list_directory_tool():
    """Test ListDirectoryTool."""
    print_section("Testing ListDirectoryTool")
    tool = ListDirectoryTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # Test with current directory
    result = tool._run(directory_path=".")
    print(f"Result (first 500 chars):\n{result[:500]}")
    print("✅ ListDirectoryTool works!")

def test_tree_tool():
    """Test TreeTool."""
    print_section("Testing TreeTool")
    tool = TreeTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # Test with src directory, max_depth 2
    result = tool._run(directory_path="src", max_depth=2)
    print(f"Result (first 500 chars):\n{result[:500]}")
    print("✅ TreeTool works!")

def test_grep_tool():
    """Test GrepTool."""
    print_section("Testing GrepTool")
    tool = GrepTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # Search for 'def' in Python files
    result = tool._run(pattern="def", directory_path="src/summercode/tools", recursive=True)
    print(f"Result (first 500 chars):\n{result[:500]}")
    print("✅ GrepTool works!")

def test_view_file_tool():
    """Test ViewFileTool."""
    print_section("Testing ViewFileTool")
    tool = ViewFileTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # View the __init__.py file
    result = tool._run(file_path="src/summercode/tools/__init__.py")
    print(f"Result (first 500 chars):\n{result[:500]}")
    print("✅ ViewFileTool works!")

def test_create_file_tool():
    """Test CreateFileTool."""
    print_section("Testing CreateFileTool")
    tool = CreateFileTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # Create a test file
    test_file = "test_create_file.txt"
    content = "Hello from CreateFileTool test!"
    result = tool._run(file_path=test_file, content=content)
    print(f"Result: {result}")
    
    # Verify it was created
    if os.path.exists(test_file):
        with open(test_file, 'r') as f:
            file_content = f.read()
        print(f"File content: {file_content}")
        os.remove(test_file)  # Clean up
        print("✅ CreateFileTool works!")
    else:
        print("❌ CreateFileTool failed - file not created")

def test_insert_content_tool():
    """Test InsertContentTool."""
    print_section("Testing InsertContentTool")
    tool = InsertContentTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # Create a test file first
    test_file = "test_insert_content.txt"
    with open(test_file, 'w') as f:
        f.write("Line 1\nLine 2\nLine 3\n")
    
    # Insert content at line 2 (before "Line 2")
    result = tool._run(
        file_path=test_file,
        line_number=2,
        content="Inserted line"
    )
    print(f"Result: {result}")
    
    # Verify insertion
    with open(test_file, 'r') as f:
        content = f.read()
    print(f"File content after insertion:\n{content}")
    os.remove(test_file)  # Clean up
    print("✅ InsertContentTool works!")

def test_str_replace_tool():
    """Test StrReplaceTool."""
    print_section("Testing StrReplaceTool")
    tool = StrReplaceTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # Create a test file
    test_file = "test_str_replace.txt"
    with open(test_file, 'w') as f:
        f.write("Hello World\nHello Python\nHello LangChain\n")
    
    # Replace "Hello" with "Hi"
    result = tool._run(
        file_path=test_file,
        old_str="Hello",
        new_str="Hi"
    )
    print(f"Result: {result}")
    
    # Verify replacement
    with open(test_file, 'r') as f:
        content = f.read()
    print(f"File content after replacement:\n{content}")
    os.remove(test_file)  # Clean up
    print("✅ StrReplaceTool works!")

def test_todo_write_tool():
    """Test TodoWriteTool."""
    print_section("Testing TodoWriteTool")
    tool = TodoWriteTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # Write multiple TODO items
    result1 = tool._run(todo_item="Task 1")
    print(f"Result 1: {result1}")
    result2 = tool._run(todo_item="Task 2", file_path="TODO.md")
    print(f"Result 2: {result2}")
    result3 = tool._run(todo_item="Task 3")
    print(f"Result 3: {result3}")
    
    # Verify TODO.md was created
    if os.path.exists("TODO.md"):
        with open("TODO.md", 'r') as f:
            content = f.read()
        print(f"TODO.md content:\n{content}")
        os.remove("TODO.md")  # Clean up
        print("✅ TodoWriteTool works!")
    else:
        print("❌ TodoWriteTool failed - TODO.md not created")

def test_bash_tool():
    """Test BashTool."""
    print_section("Testing BashTool")
    tool = BashTool()
    print(f"Tool name: {tool.name}")
    print(f"Description: {tool.description}")
    
    # Run a simple command
    if os.name == 'nt':  # Windows
        result = tool._run(command="echo Hello from BashTool")
    else:  # Unix-like
        result = tool._run(command="echo 'Hello from BashTool'")
    
    print(f"Result: {result}")
    print("✅ BashTool works!")

def main():
    """Run all tool tests."""
    print("\n" + "🔧" * 30)
    print("  SummerCode Tools Test Suite")
    print("🔧" * 30)
    
    try:
        test_list_directory_tool()
        test_tree_tool()
        test_grep_tool()
        test_view_file_tool()
        test_create_file_tool()
        test_insert_content_tool()
        test_str_replace_tool()
        test_todo_write_tool()
        test_bash_tool()
        
        print_section("🎉 All Tests Passed!")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
