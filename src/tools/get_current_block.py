"""Return the block where the cursor is currently positioned in Logseq."""

from typing import List

from mcp.types import TextContent

from src.client.config import LogseqConfig
from src.client.logseq_client import LogseqClient
from src.logging_setup import get_logger

_log = get_logger(__name__)


async def get_current_block(
    client: LogseqClient,
    config: LogseqConfig,
) -> List[TextContent]:
    """Return the block where the cursor is currently positioned in Logseq.

    Returns:
        TextContent with the block UUID, content, and parent page.
        Returns a 'No active block' message when no block is being edited.
    """
    try:
        _log.debug("%s called", __name__)
        block = await client.get_current_block()
        if not block:
            return [TextContent(type="text", text="No active block in Logseq editor.")]

        uuid = block.get("uuid", "")
        content = block.get("content", "")
        page_info = block.get("page", {})
        page_name = (
            page_info.get("originalName") or page_info.get("name", "")
            if isinstance(page_info, dict)
            else ""
        )

        text = (
            f"## Current Block\n\n"
            f"**UUID:** {uuid}\n"
            f"**Page:** {page_name}\n\n"
            f"**Content:**\n```\n{content}\n```\n"
        )
        return [TextContent(type="text", text=text)]

    except Exception as exc:
        _log.error("exception in %s: %s", __name__, exc, exc_info=True)
        return [TextContent(type="text", text=f"❌ Error getting current block: {exc}")]
