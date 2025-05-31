from mcp.server.fastmcp import FastMCP
from tools import get_all_page_content
from tools import get_all_pages
from tools import get_page_blocks
from tools import get_block_content
from tools import get_page_links
from tools import get_linked_flashcards


def register_all_tools(mcp_server: FastMCP) -> None:
    """
    Register all tools with the MCP server.

    Args:
        mcp_server: The FastMCP server instance to register tools with
    """

    # Add more tools here as you create them
    mcp_server.tool()(get_all_page_content)
    mcp_server.tool()(get_all_pages)
    mcp_server.tool()(get_page_blocks)
    mcp_server.tool()(get_block_content)
    mcp_server.tool()(get_page_links)
    mcp_server.tool()(get_linked_flashcards)
