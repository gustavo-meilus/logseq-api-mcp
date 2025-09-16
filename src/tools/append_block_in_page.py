import os
from pathlib import Path
from typing import Any, List, Optional

import aiohttp
from dotenv import load_dotenv
from mcp.types import TextContent

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def append_block_in_page(
    page_identifier: str,
    content: str,
    before: Optional[str] = None,
    sibling: Optional[str] = None,
    is_page_block: Optional[bool] = None,
) -> List[TextContent]:
    """
    Append a new block to a specified page in Logseq.

    This tool allows you to add new content blocks to any page in your Logseq graph.
    You can specify positioning options to control where the block is inserted.

    Args:
        page_identifier: The name or UUID of the page to append the block to
        content: The content of the block to append
        before: Optional UUID of a block to insert before
        sibling: Optional UUID of a sibling block for positioning
        is_page_block: Optional boolean to indicate if this is a page-level block
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    # Build options object
    options: dict[str, Any] = {}
    if before is not None:
        options["before"] = before
    if sibling is not None:
        options["sibling"] = sibling
    if is_page_block is not None:
        options["isPageBlock"] = is_page_block

    async with aiohttp.ClientSession() as session:
        try:
            # Prepare the API call
            payload = {
                "method": "logseq.Editor.appendBlockInPage",
                "args": [page_identifier, content, options]
                if options
                else [page_identifier, content],
            }

            async with session.post(
                endpoint, json=payload, headers=headers
            ) as response:
                if response.status != 200:
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Failed to append block: HTTP {response.status}",
                        )
                    ]

                result = await response.json()

                # Check if the result indicates success
                if result is None or result == "":
                    return [
                        TextContent(
                            type="text",
                            text="❌ Failed to append block: No response from Logseq API",
                        )
                    ]

                # Build success response
                output_lines = [
                    "✅ **BLOCK APPENDED SUCCESSFULLY**",
                    f"📄 Page: {page_identifier}",
                    f"📝 Content: {content}",
                    "",
                ]

                # Add positioning info if specified
                if before:
                    output_lines.append(f"📍 Positioned before block: {before}")
                if sibling:
                    output_lines.append(f"📍 Positioned as sibling of: {sibling}")
                if is_page_block:
                    output_lines.append("📍 Block type: Page-level block")

                if not (before or sibling or is_page_block):
                    output_lines.append("📍 Positioned: At the end of the page")

                output_lines.extend(
                    [
                        "",
                        "🔗 **NEXT STEPS:**",
                        "• Check your Logseq graph to see the new block",
                        "• Use get_page_blocks to verify the block was added",
                        "• Use get_block_content to get details of the new block",
                    ]
                )

                return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [
                TextContent(type="text", text=f"❌ Error appending block: {str(e)}")
            ]
