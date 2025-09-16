import os
from pathlib import Path
from typing import List

import aiohttp
from dotenv import load_dotenv
from mcp.types import TextContent

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def get_block_content(block_uuid: str) -> List[TextContent]:
    """
    Get detailed content and metadata for a specific block using its UUID.

    Returns comprehensive block information formatted for optimal LLM consumption
    including properties, relationships, and content.

    Args:
        block_uuid: The UUID of the block to retrieve
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    def format_properties(props):
        """Format block properties into a readable display"""
        if not props:
            return "None"

        formatted_props = []
        for property_name, value in props.items():
            if isinstance(value, list):
                value_str = ", ".join(str(v) for v in value)
            else:
                value_str = str(value)
            formatted_props.append(f"**{property_name}**: {value_str}")

        return "\n".join(formatted_props)

    def format_children_summary(children):
        """Format children summary information"""
        if not children:
            return "None"

        children_info = []
        for child in children:
            if isinstance(child, list) and len(child) >= 2:
                if child[0] == "uuid":
                    children_info.append(f"Block UUID: {child[1]}")
                else:
                    children_info.append(f"{child[0]}: {child[1]}")
            else:
                children_info.append(str(child))

        return "\n".join(children_info)

    def format_content_display(content, block_type_prefix=""):
        """Format content for clear display"""
        if not content:
            return "[Empty block]"

        # Clean up content for display
        content = content.strip()

        # Identify content type
        if content.startswith("#"):
            content_type = "📑 Header"
        elif "#card" in content:
            content_type = "💡 Flashcard"
        elif content.startswith("```"):
            content_type = "💻 Code Block"
        elif content.startswith("- ") or content.startswith("* "):
            content_type = "📝 List Item"
        elif "::" in content and len(content.split("\n")[0]) < 50:
            content_type = "⚙️ Properties"
        else:
            content_type = "📄 Text Block"

        # Add prefix for child blocks
        if block_type_prefix:
            content_type = f"{block_type_prefix} {content_type}"

        # Format based on length
        if len(content) > 500:
            preview = content[:500] + "..."
            return f"{content_type}\n**Content** ({len(content)} chars):\n{preview}\n\n*[Content truncated - showing first 500 characters]*"
        else:
            return f"{content_type}\n**Content:**\n{content}"

    async def get_block_by_uuid(session, uuid):
        """Helper function to get a block by UUID"""
        payload = {"method": "logseq.Editor.getBlock", "args": [uuid]}
        async with session.post(endpoint, json=payload, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return None

    def format_block_details(block, is_child=False):
        """Format block details consistently"""
        if not block:
            return []

        # Extract block information
        block_id = block.get("id", "N/A")
        uuid = block.get("uuid", "N/A")
        content = block.get("content", "")
        properties = block.get("properties", {})
        children = block.get("children", [])
        parent = block.get("parent", {})
        page = block.get("page", {})

        # Get parent and page info
        parent_id = parent.get("id", "N/A") if parent else "N/A"
        page_id = page.get("id", "N/A") if page else "N/A"
        page_name = page.get("name", "Unknown") if page else "Unknown"

        # Build block details
        prefix = "👶 **CHILD BLOCK**" if is_child else "🔍 **MAIN BLOCK**"
        lines = [
            prefix,
            f"📌 Block ID: {block_id}",
            f"🔑 UUID: {uuid}",
            "",
        ]

        if not is_child:
            lines.extend(
                [
                    "📄 **PAGE CONTEXT:**",
                    f"• Page: {page_name} (ID: {page_id})",
                    f"• Parent Block ID: {parent_id}",
                    "",
                ]
            )

        lines.extend(
            [
                "⚙️ **PROPERTIES:**",
                format_properties(properties),
                "",
                "📝 **CONTENT:**",
                format_content_display(content, "🔸" if is_child else ""),
                "",
            ]
        )

        if not is_child:
            lines.extend(
                [
                    "👶 **IMMEDIATE CHILDREN:**",
                    f"Count: {len(children)}",
                    format_children_summary(children)
                    if children
                    else "No child blocks",
                    "",
                ]
            )

        lines.extend(
            [
                "📊 **TECHNICAL SUMMARY:**",
                f"• Block Type: {'Header' if content.startswith('#') else 'Flashcard' if '#card' in content else 'Code' if content.startswith('```') else 'Text'}",
                f"• Has Properties: {'Yes' if properties else 'No'}",
                f"• Has Children: {'Yes' if children else 'No'}",
                f"• Content Length: {len(content)} characters",
                "",
            ]
        )

        return lines

    async with aiohttp.ClientSession() as session:
        try:
            # Get main block by UUID
            main_block = await get_block_by_uuid(session, block_uuid)
            if not main_block:
                return [
                    TextContent(
                        type="text",
                        text=f"❌ Block with UUID '{block_uuid}' not found",
                    )
                ]

            # Start building output with main block
            output_lines = format_block_details(main_block, is_child=False)

            # Get immediate children blocks
            children = main_block.get("children", [])
            if children:
                output_lines.extend(
                    [
                        "=" * 60,
                        "🌳 **IMMEDIATE CHILDREN DETAILS:**",
                        "",
                    ]
                )

                for i, child in enumerate(children, 1):
                    # Extract UUID from child reference
                    child_uuid = None
                    if (
                        isinstance(child, list)
                        and len(child) >= 2
                        and child[0] == "uuid"
                    ):
                        child_uuid = child[1]
                    elif isinstance(child, dict):
                        child_uuid = child.get("uuid")

                    if child_uuid:
                        child_block = await get_block_by_uuid(session, child_uuid)
                        if child_block:
                            output_lines.extend(
                                [
                                    f"🔸 **CHILD {i}:**",
                                    "",
                                ]
                            )
                            output_lines.extend(
                                format_block_details(child_block, is_child=True)
                            )
                            output_lines.append("-" * 40)
                        else:
                            output_lines.extend(
                                [
                                    f"🔸 **CHILD {i}:**",
                                    f"❌ Could not fetch child block with UUID: {child_uuid}",
                                    "-" * 40,
                                ]
                            )
                    else:
                        output_lines.extend(
                            [
                                f"🔸 **CHILD {i}:**",
                                f"❌ Invalid child reference: {child}",
                                "-" * 40,
                            ]
                        )

            return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [
                TextContent(
                    type="text", text=f"❌ Error fetching block content: {str(e)}"
                )
            ]
