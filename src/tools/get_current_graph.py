"""Return metadata for the currently active Logseq graph."""

from typing import List

from mcp.types import TextContent

from src.client.config import LogseqConfig
from src.client.logseq_client import LogseqClient
from src.logging_setup import get_logger

_log = get_logger(__name__)


async def get_current_graph(
    client: LogseqClient,
    config: LogseqConfig,
) -> List[TextContent]:
    """Return metadata for the currently active Logseq graph.

    Returns:
        TextContent with the graph name, filesystem path, and URL.
        Returns a 'No active graph' message when Logseq returns empty data.
    """
    try:
        _log.debug("%s called", __name__)
        graph = await client.get_current_graph()
        if not graph:
            return [TextContent(type="text", text="No active graph in Logseq.")]

        name = graph.get("name", "")
        path = graph.get("path", "")
        url = graph.get("url", "")

        text = (
            f"## Current Graph\n\n**Name:** {name}\n**Path:** {path}\n**URL:** {url}\n"
        )
        return [TextContent(type="text", text=text)]

    except Exception as exc:
        _log.error("exception in %s: %s", __name__, exc, exc_info=True)
        return [TextContent(type="text", text=f"❌ Error getting current graph: {exc}")]
