"""Return the blocks currently selected in the Logseq editor."""

from typing import List

from mcp.types import TextContent

from src.client.config import LogseqConfig
from src.client.logseq_client import LogseqClient
from src.logging_setup import get_logger

_log = get_logger(__name__)


async def get_editing_selection(
    client: LogseqClient,
    config: LogseqConfig,
) -> List[TextContent]:
    """Return the blocks currently selected in the Logseq editor.

    Returns:
        TextContent listing all selected blocks with their UUID and content.
        Returns a 'No blocks selected' message when no selection is active.
    """
    try:
        _log.debug("%s called", __name__)
        blocks = await client.get_editing_selection()
        if not blocks:
            return [
                TextContent(type="text", text="No blocks selected in Logseq editor.")
            ]

        lines = [f"## Selected Blocks ({len(blocks)})\n"]
        for i, block in enumerate(blocks, start=1):
            uuid = block.get("uuid", "")
            content = block.get("content", "")
            lines.append(f"### Block {i}\n**UUID:** {uuid}\n```\n{content}\n```\n")

        return [TextContent(type="text", text="\n".join(lines))]

    except Exception as exc:
        _log.error("exception in %s: %s", __name__, exc, exc_info=True)
        return [
            TextContent(type="text", text=f"❌ Error getting editing selection: {exc}")
        ]
