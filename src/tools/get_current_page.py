"""Return the page currently open in the Logseq editor."""

from typing import List

from mcp.types import TextContent

from src.client.config import LogseqConfig
from src.client.logseq_client import LogseqClient
from src.logging_setup import get_logger

_log = get_logger(__name__)


async def get_current_page(
    client: LogseqClient,
    config: LogseqConfig,
) -> List[TextContent]:
    """Return the page currently open in the Logseq editor.

    Returns:
        TextContent with the active page name, UUID, and type (journal or standard).
        Returns a 'No active page' message when no page is open.
    """
    try:
        _log.debug("%s called", __name__)
        page = await client.get_current_page()
        if not page:
            return [TextContent(type="text", text="No active page in Logseq editor.")]

        name = page.get("originalName") or page.get("name", "(unnamed)")
        uuid = page.get("uuid", "")
        is_journal = page.get("journal?", False)
        page_type = "Journal" if is_journal else "Page"

        text = (
            f"## Current Page\n\n"
            f"**Name:** {name}\n"
            f"**UUID:** {uuid}\n"
            f"**Type:** {page_type}\n"
        )
        return [TextContent(type="text", text=text)]

    except Exception as exc:
        _log.error("exception in %s: %s", __name__, exc, exc_info=True)
        return [TextContent(type="text", text=f"❌ Error getting current page: {exc}")]
