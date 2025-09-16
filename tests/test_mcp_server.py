"""Tests for MCP server functionality."""

from src.registry import register_all_tools
from src.server import mcp


class TestMCPServer:
    """Test cases for MCP server functionality."""

    def test_server_initialization(self):
        """Test that the MCP server can be initialized."""
        assert mcp is not None
        assert hasattr(mcp, "list_tools")

    def test_tool_registration(self):
        """Test that all tools are properly registered."""
        # Get the list of registered tools
        tools = mcp.list_tools()

        # Check that we have the expected number of tools
        assert len(tools) >= 9

        # Check for specific tools
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "append_block_in_page",
            "create_page",
            "edit_block",
            "get_all_pages",
            "get_page_blocks",
            "get_block_content",
            "get_all_page_content",
            "get_page_links",
            "get_linked_flashcards",
        ]

        for expected_tool in expected_tools:
            assert expected_tool in tool_names, (
                f"Tool {expected_tool} not found in registered tools"
            )

    def test_register_all_tools_function(self):
        """Test the register_all_tools function."""
        # This should not raise any exceptions
        register_all_tools(mcp)

        # Verify tools are still registered
        tools = mcp.list_tools()
        assert len(tools) >= 9
