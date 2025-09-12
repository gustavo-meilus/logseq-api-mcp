import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiohttp
from dotenv import load_dotenv
from mcp.types import TextContent

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def edit_block(
    block_identity: str,
    content: Optional[str] = None,
    properties: Optional[Dict[str, Any]] = None,
    cursor_position: Optional[int] = None,
    focus: Optional[bool] = None,
) -> List[TextContent]:
    """
    Edit a block in Logseq.

    This tool allows you to edit existing blocks in your Logseq graph by updating
    their content, properties, or cursor position. The block can be identified
    by its UUID or by providing a BlockIdentity object.

    Args:
        block_identity: The UUID of the block to edit (BlockIdentity)
        content: Optional new content for the block
        properties: Optional dictionary of properties to update on the block
        cursor_position: Optional cursor position for editing (0-based index)
        focus: Optional boolean to focus the block after editing
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    # Build options object
    options: Dict[str, Any] = {}
    if cursor_position is not None:
        options["pos"] = cursor_position
    if focus is not None:
        options["focus"] = focus

    # Prepare the arguments for the API call
    args = [block_identity]

    # Add content if provided
    if content is not None:
        args.append(content)

    # Add properties if provided
    if properties is not None:
        args.append(properties)

    # Add options if any
    if options:
        args.append(options)

    async with aiohttp.ClientSession() as session:
        try:
            # Prepare the API call
            payload = {
                "method": "logseq.Editor.editBlock",
                "args": args,
            }

            async with session.post(
                endpoint, json=payload, headers=headers
            ) as response:
                if response.status != 200:
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Failed to edit block: HTTP {response.status}",
                        )
                    ]

                result = await response.json()

                # Check if the result indicates success
                if result is None or result == "":
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Failed to edit block: No response from Logseq API",
                        )
                    ]

                # Build success response
                output_lines = [
                    "✅ **BLOCK EDITED SUCCESSFULLY**",
                    f"🔗 Block UUID: {block_identity}",
                    "",
                ]

                # Add edit details
                edit_details = []
                if content is not None:
                    edit_details.append(f"📝 Content updated")
                if properties is not None:
                    edit_details.append(
                        f"⚙️ Properties updated ({len(properties)} items)"
                    )
                if cursor_position is not None:
                    edit_details.append(
                        f"📍 Cursor positioned at index {cursor_position}"
                    )
                if focus is not None:
                    edit_details.append(
                        f"🎯 Focus: {'Enabled' if focus else 'Disabled'}"
                    )

                if edit_details:
                    output_lines.extend(
                        [
                            "📊 **EDIT DETAILS:**",
                            *[f"• {detail}" for detail in edit_details],
                            "",
                        ]
                    )

                # Add content preview if updated
                if content is not None:
                    content_preview = (
                        content[:100] + "..." if len(content) > 100 else content
                    )
                    output_lines.extend(
                        [
                            "📝 **UPDATED CONTENT:**",
                            f"```",
                            content_preview,
                            "```",
                            "",
                        ]
                    )

                # Add properties if updated
                if properties is not None:
                    output_lines.extend(
                        [
                            "⚙️ **UPDATED PROPERTIES:**",
                            *[f"• {key}: {value}" for key, value in properties.items()],
                            "",
                        ]
                    )

                # Add result details if available
                if isinstance(result, dict):
                    result_id = result.get("id", "N/A")
                    result_uuid = result.get("uuid", block_identity)
                    result_content = result.get("content", "")

                    if result_id != "N/A" or result_uuid != block_identity:
                        output_lines.extend(
                            [
                                "📋 **BLOCK INFORMATION:**",
                                f"• ID: {result_id}",
                                f"• UUID: {result_uuid}",
                                "",
                            ]
                        )

                output_lines.extend(
                    [
                        "🔗 **NEXT STEPS:**",
                        "• Check your Logseq graph to see the updated block",
                        "• Use get_block_content to verify the changes",
                        "• Use get_page_blocks to see the block in context",
                    ]
                )

                return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error editing block: {str(e)}")]
