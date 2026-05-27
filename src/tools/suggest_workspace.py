"""Generate Claude Code workspace config for the active Logseq graph."""

from typing import List

from mcp.types import TextContent

from src.client.config import LogseqConfig
from src.client.logseq_client import LogseqClient
from src.logging_setup import get_logger
from src.workspace.configurator import WorkspaceConfigurator

_log = get_logger(__name__)


async def suggest_workspace(
    client: LogseqClient,
    config: LogseqConfig,
) -> List[TextContent]:
    """Generate Claude Code workspace config for the active Logseq graph.

    Reads the currently active Logseq graph path and produces:
    - A .mcp.json file content pre-filled with your API token and URL
    - The target path where the file should be written
    - A one-liner claude mcp add-json install command

    Once .mcp.json is written to your graph folder, running 'claude' from that
    folder will automatically connect all Logseq MCP tools.

    Returns:
        TextContent with setup instructions, .mcp.json content, and install command.
    """
    try:
        _log.debug("%s called", __name__)
        graph = await client.get_current_graph()
        if not graph:
            return [
                TextContent(
                    type="text",
                    text=(
                        "No active graph in Logseq. "
                        "Open a graph in Logseq and try again."
                    ),
                )
            ]

        wc = WorkspaceConfigurator(graph_info=graph, config=config)
        graph_path = graph.get("path", "")
        graph_name = graph.get("name", "")
        target = wc.target_path()
        mcp_json = wc.mcp_json_content()
        install_cmd = wc.install_command()

        text = (
            f"## Claude Code Workspace Setup\n\n"
            f"**Graph:** {graph_name}\n"
            f"**Graph path:** {graph_path}\n\n"
            f"---\n\n"
            f"### Option A — Write .mcp.json (auto-connect on every session)\n\n"
            f"Write this content to `{target}`:\n\n"
            f"```json\n{mcp_json}\n```\n\n"
            f"Then run Claude Code from your graph folder:\n\n"
            f"```bash\ncd {graph_path}\nclaude\n```\n\n"
            f"Claude Code will auto-connect all Logseq tools on startup.\n\n"
            f"---\n\n"
            f"### Option B — One-time install command\n\n"
            f"Run this once to register the MCP server globally:\n\n"
            f"```bash\n{install_cmd}\n```\n"
        )
        return [TextContent(type="text", text=text)]

    except Exception as exc:
        _log.error("exception in %s: %s", __name__, exc, exc_info=True)
        return [
            TextContent(
                type="text", text=f"❌ Error generating workspace config: {exc}"
            )
        ]
