from mcp.server.fastmcp import FastMCP
import tools


def register_all_tools(mcp_server: FastMCP) -> None:
    """
    Register all tools with the MCP server.

    Dynamically discovers and registers all functions from the tools module.

    Args:
        mcp_server: The FastMCP server instance to register tools with
    """

    # Dynamically register all tools found in the tools module
    for tool_name in tools.__all__:
        tool_function = getattr(tools, tool_name)
        mcp_server.tool()(tool_function)
