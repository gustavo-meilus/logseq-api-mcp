import os
from pathlib import Path
from typing import List

import aiohttp
from dotenv import load_dotenv
from mcp.types import TextContent

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def get_page_blocks(page_identifier: str) -> List[TextContent]:
    """
    Get the tree structure of blocks that compose a page in Logseq.

    Returns a hierarchical view of all blocks with their essential metadata,
    formatted for optimal LLM consumption with clear tree visualization.

    Args:
        page_identifier: The name or UUID of the page to get blocks from
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    def format_properties(props):
        """Format block properties into a concise display"""
        if not props:
            return ""

        # Filter out less important properties for concise display
        important_props = {}
        for property_name, value in props.items():
            if property_name not in [
                "collapsed",
                "card-last-interval",
                "card-repeats",
                "card-ease-factor",
                "card-next-schedule",
                "card-last-reviewed",
            ]:
                if isinstance(value, list):
                    important_props[property_name] = ", ".join(str(v) for v in value)
                elif value:
                    important_props[property_name] = str(value)

        if important_props:
            prop_items = [
                f"{prop_name}: {prop_value}"
                for prop_name, prop_value in list(important_props.items())[:3]
            ]
            return f" [{'; '.join(prop_items)}]"
        return ""

    def format_content_preview(content, max_length=100):
        """Create a clean preview of block content"""
        if not content:
            return "[empty]"

        # Clean up the content
        content = content.strip()
        content = content.replace("\n", " ").replace("\r", " ")

        # Remove card markers for cleaner display
        if "#card" in content:
            content = content.replace("#card", "").strip()
            content = f"💡 {content}"

        # Truncate if too long
        if len(content) > max_length:
            content = content[:max_length] + "..."

        return content

    def format_block_tree(block, level=0, max_level=10):
        """Recursively format blocks into a tree structure"""
        if level > max_level:
            return []

        lines = []
        indent = "  " * level

        # Get block info
        block_id = block.get("id", "N/A")
        uuid = block.get("uuid", "N/A")
        content = block.get("content", "")
        properties = block.get("properties", {})
        children = block.get("children", [])
        block_level = block.get("level", level)
        is_pre_block = block.get("preBlock?", False)

        # Determine block type emoji
        if content.startswith("#"):
            emoji = "📑"
            if "# " in content:
                header_level = len(content.split("#")[0]) + 1
                emoji = f"H{header_level}"
        elif "#card" in content:
            emoji = "💡"
        elif is_pre_block:
            emoji = "📋"
        elif properties:
            emoji = "⚙️"
        else:
            emoji = "•"

        # Format the main block line
        content_preview = format_content_preview(content)
        props_display = format_properties(properties)

        block_line = f"{indent}{emoji} {content_preview}"
        if props_display:
            block_line += props_display

        # Add technical details
        tech_details = f"ID:{block_id} | UUID:{uuid} | Level:{block_level}"
        if is_pre_block:
            tech_details += " | PreBlock"

        lines.append(f"{block_line}")
        lines.append(f"{indent}   📊 {tech_details}")

        # Add parent info if available
        parent = block.get("parent", {})
        if parent and parent.get("id"):
            lines.append(f"{indent}   👆 Parent ID: {parent.get('id')}")

        # Add children count
        if children:
            lines.append(f"{indent}   👇 Children: {len(children)}")

        lines.append("")  # Empty line for separation

        # Recursively format children
        for child in children:
            lines.extend(format_block_tree(child, level + 1, max_level))

        return lines

    async with aiohttp.ClientSession() as session:
        try:
            # Get page blocks tree
            payload = {
                "method": "logseq.Editor.getPageBlocksTree",
                "args": [page_identifier],
            }

            async with session.post(
                endpoint, json=payload, headers=headers
            ) as response:
                if response.status != 200:
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Failed to fetch page blocks: HTTP {response.status}",
                        )
                    ]

                blocks = await response.json()
                if not blocks:
                    return [
                        TextContent(
                            type="text",
                            text=f"✅ Page '{page_identifier}' has no blocks",
                        )
                    ]

            # Get page info from first block
            page_info = blocks[0].get("page", {}) if blocks else {}
            page_name = page_info.get("name", page_identifier)
            page_id = page_info.get("id", "N/A")

            # Build output
            output_lines = [
                "🌳 **PAGE BLOCKS TREE STRUCTURE**",
                f"📄 Page: {page_name} (ID: {page_id})",
                f"📊 Total blocks: {len(blocks)}",
                "",
                "🔗 **TREE HIERARCHY:**",
                "",
            ]

            # Format all blocks in tree structure
            for block in blocks:
                output_lines.extend(format_block_tree(block, 0, max_level=8))

            # Add summary
            output_lines.extend(
                [
                    "📈 **SUMMARY:**",
                    f"• Total blocks processed: {len(blocks)}",
                    "• Tree depth: Variable (max 8 levels shown)",
                    "• Format: Hierarchical with metadata",
                    "",
                ]
            )

            return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [
                TextContent(
                    type="text", text=f"❌ Error fetching page blocks: {str(e)}"
                )
            ]
