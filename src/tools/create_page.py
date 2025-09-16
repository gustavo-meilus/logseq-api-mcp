import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
from dotenv import load_dotenv
from mcp.types import TextContent

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def create_page(
    page_name: str,
    properties: Optional[Dict[str, Any]] = None,
    format: Optional[str] = None,
) -> List[TextContent]:
    """
    Create a new page in Logseq.

    This tool allows you to create new pages in your Logseq graph with optional
    properties and format specifications. The page will be created and can be
    immediately used for adding content.

    Args:
        page_name: The name of the page to create
        properties: Optional dictionary of properties to set on the page
        format: Optional format for the page ("markdown" or "org")
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    # Build options object
    options = {}
    if properties:
        options["properties"] = properties
    if format:
        options["format"] = format

    async with aiohttp.ClientSession() as session:
        try:
            # Prepare the API call
            payload = {
                "method": "logseq.Editor.createPage",
                "args": [page_name, options] if options else [page_name],
            }

            async with session.post(
                endpoint, json=payload, headers=headers
            ) as response:
                if response.status != 200:
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Failed to create page: HTTP {response.status}",
                        )
                    ]

                result = await response.json()

                # Check if the result indicates success
                if result is None or result == "":
                    return [
                        TextContent(
                            type="text",
                            text="❌ Failed to create page: No response from Logseq API",
                        )
                    ]

                # Build success response
                output_lines = [
                    "✅ **PAGE CREATED SUCCESSFULLY**",
                    f"📄 Page Name: {page_name}",
                    "",
                ]

                # Add page details if available
                if isinstance(result, dict):
                    page_id = result.get("id", "N/A")
                    page_uuid = result.get("uuid", "N/A")
                    original_name = result.get("originalName", page_name)
                    is_journal = result.get("journal?", False)
                    page_format = result.get("format", "markdown")

                    output_lines.extend(
                        [
                            "📊 **PAGE DETAILS:**",
                            f"• ID: {page_id}",
                            f"• UUID: {page_uuid}",
                            f"• Original Name: {original_name}",
                            f"• Format: {page_format}",
                            f"• Journal Page: {'Yes' if is_journal else 'No'}",
                            "",
                        ]
                    )

                    # Add properties if available
                    page_properties = result.get("properties", {})
                    if page_properties:
                        output_lines.extend(
                            [
                                "⚙️ **PAGE PROPERTIES:**",
                                *[
                                    f"• {key}: {value}"
                                    for key, value in page_properties.items()
                                ],
                                "",
                            ]
                        )

                # Add creation info
                if properties:
                    output_lines.append(f"⚙️ Properties set: {len(properties)} items")
                if format:
                    output_lines.append(f"📝 Format: {format}")

                output_lines.extend(
                    [
                        "",
                        "🔗 **NEXT STEPS:**",
                        "• Check your Logseq graph to see the new page",
                        "• Use get_all_pages to verify the page was created",
                        "• Use append_block_in_page to add content to the page",
                        "• Use get_page_blocks to view the page structure",
                    ]
                )

                return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error creating page: {str(e)}")]
