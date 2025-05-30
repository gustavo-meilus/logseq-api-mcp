from mcp.server.fastmcp import FastMCP
from registry import register_all_tools

# Create an MCP server
mcp = FastMCP("Logseq API")

# Register all tools
register_all_tools(mcp)

if __name__ == "__main__":
    mcp.run()
