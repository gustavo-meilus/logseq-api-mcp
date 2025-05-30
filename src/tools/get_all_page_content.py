import os
import aiohttp
from typing import List
from mcp.types import TextContent
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def get_all_page_content(page_identifier: str) -> List[TextContent]:
    """
    Get comprehensive page content including all blocks, their full content, and linked references.

    Args:
        page_identifier: The name or UUID of the page to get complete content from
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    def get_content_preview(content, max_length=300):
        """Get a clean preview of content with expanded limits"""
        if not content:
            return "[No content]"

        content = content.strip()
        lines = content.split("\n")
        meaningful_lines = []

        for line in lines:
            line = line.strip()
            if line and not line.startswith("::") and not line.startswith("card-"):
                if "collapsed::" not in line and "card-" not in line:
                    meaningful_lines.append(line)

        preview = " ".join(meaningful_lines)
        preview = preview.replace("[[", "").replace("]]", "")
        preview = preview.replace("#card", "").strip()

        return preview[:max_length] + "..." if len(preview) > max_length else preview

    def format_essential_properties(props):
        """Format essential properties based on common patterns rather than language-specific keys"""
        if not props:
            return []

        formatted = []

        # Look for common property patterns (language-agnostic)
        for key, value in props.items():
            if not value:
                continue

            # Convert to string if it's a list
            if isinstance(value, list):
                value_str = ", ".join(str(v) for v in value)
            else:
                value_str = str(value)

            # Only show non-empty, meaningful properties
            # Skip only technical/system properties that clutter the display
            if (
                key
                not in [
                    "collapsed",
                    "card-last-interval",
                    "card-repeats",
                    "card-ease-factor",
                    "card-next-schedule",
                    "card-last-reviewed",
                    "card-last-score",
                    "id",
                    "uuid",
                    "created-at",
                    "updated-at",
                ]
                and len(value_str.strip()) > 0
                and value_str.strip() != "nil"
                and value_str.strip() != "null"
            ):
                formatted.append(f"{key}: {value_str}")

        # Show more properties to be inclusive - increase limit
        return formatted[:8]

    def format_flashcard_content(content):
        """Format flashcard content as clean Q&A"""
        if "#card" not in content:
            return content

        # Remove #card tag and clean up
        clean_content = content.replace("#card", "").strip()

        # Try to split into Q&A
        if "\n" in clean_content:
            lines = clean_content.split("\n")
            question = lines[0].strip()
            answer = "\n".join(lines[1:]).strip()

            if question and answer:
                return f"❓ **Q:** {question}\n💡 **A:** {answer}"

        return f"🎯 **Flashcard:** {clean_content}"

    def format_block_with_content(block, indent_level=0, max_depth=6):
        """Recursively format blocks with deep content extraction for technical content"""
        if indent_level > max_depth:
            return []

        indent = "   " * indent_level
        lines = []

        # Get block info
        block_id = block.get("id")
        content = block.get("content", "").strip()
        properties = block.get("properties", {})

        # Choose emoji based on content type and structure
        if indent_level == 0:
            emoji = "📄"
        elif content.startswith("#"):
            # Detect content type by structure and common patterns
            content_lower = content.lower()
            if any(
                word in content_lower
                for word in ["topics", "table of contents", "index"]
            ):
                emoji = "📚"
            elif any(
                word in content_lower
                for word in ["notes", "annotations", "observations"]
            ):
                emoji = "📝"
            elif any(word in content_lower for word in ["flashcards", "cards", "quiz"]):
                emoji = "🎯"
            elif any(
                word in content_lower for word in ["summary", "overview", "abstract"]
            ):
                emoji = "📋"
            elif any(
                word in content_lower
                for word in ["implementation", "code", "development"]
            ):
                emoji = "⚙️"
            elif any(
                word in content_lower
                for word in ["services", "entities", "value objects", "architecture"]
            ):
                emoji = "🔧"
            else:
                emoji = "📑"
        elif "#card" in content:
            emoji = "💡"
        elif "```" in content:  # Code blocks
            emoji = "💻"
        else:
            emoji = "•"

        # Block title and content handling - ALWAYS process every block
        if content:
            if "#card" in content:
                # Special handling for flashcards
                lines.append(f"{indent}{emoji} **Flashcard** [{block_id}]")
                formatted_card = format_flashcard_content(content)
                lines.append(f"{indent}   {formatted_card}")
            else:
                first_line = content.split("\n")[0].strip()
                if first_line.startswith("#"):
                    title = first_line
                elif "::" in first_line and indent_level == 0:
                    title = "Page Properties"
                else:
                    title = (
                        first_line[:100] + "..."
                        if len(first_line) > 100
                        else first_line
                    )

                lines.append(f"{indent}{emoji} **{title}** [{block_id}]")

                # Show essential properties for top-level blocks (always include if present)
                if properties and indent_level == 0:
                    essential_props = format_essential_properties(properties)
                    if essential_props:
                        lines.append(f"{indent}   📋 {' | '.join(essential_props)}")

                # Expanded content handling - ALWAYS show content when substantial
                if not content.startswith("#") and len(content) > 100:  # Not a header
                    # Special handling for code blocks - preserve fully
                    if "```" in content:
                        lines.append(f"{indent}   💻 **Code Block:**")
                        lines.append(f"{indent}   {content}")
                    elif (
                        len(content) > 2000
                    ):  # Very large content - show substantial portion
                        lines.append(
                            f"{indent}   📄 **Content** ({len(content)} chars):"
                        )
                        lines.append(f"{indent}   {content[:2000]}...")
                        lines.append(
                            f"{indent}   *[Content continues for {len(content) - 2000} more characters]*"
                        )
                    else:
                        lines.append(f"{indent}   📄 {content}")
        else:
            # ALWAYS show empty blocks too - they may be structurally important
            lines.append(f"{indent}{emoji} [Empty block] [{block_id}]")

        # Enhanced children handling - show much more content
        children = block.get("children", [])
        if children and indent_level < max_depth:
            # Dramatically reduce truncation for technical content
            if indent_level <= 2:
                # Show ALL children for important sections
                for child in children:
                    lines.extend(
                        format_block_with_content(child, indent_level + 1, max_depth)
                    )
            elif indent_level <= 4:
                # Show first 10 children for deeper sections
                for child in children[:10]:
                    lines.extend(
                        format_block_with_content(child, indent_level + 1, max_depth)
                    )
                if len(children) > 10:
                    lines.append(
                        f"{indent}   ... and {len(children) - 10} more child blocks"
                    )
            else:
                # Show first 5 for very deep sections
                for child in children[:5]:
                    lines.extend(
                        format_block_with_content(child, indent_level + 1, max_depth)
                    )
                if len(children) > 5:
                    lines.append(
                        f"{indent}   ... and {len(children) - 5} more child blocks"
                    )

        lines.append("")  # Add spacing
        return lines

    async with aiohttp.ClientSession() as session:
        try:
            # 1. Get page blocks
            blocks_payload = {
                "method": "logseq.Editor.getPageBlocksTree",
                "args": [page_identifier],
            }
            async with session.post(
                endpoint, json=blocks_payload, headers=headers
            ) as response:
                if response.status != 200:
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Failed to fetch page blocks: {response.status}",
                        )
                    ]

                blocks = await response.json()
                if not blocks:
                    return [
                        TextContent(
                            type="text",
                            text=f"✅ Page: {page_identifier} - No content found",
                        )
                    ]

            # 2. Get page links
            links_payload = {
                "method": "logseq.Editor.getPageLinkedReferences",
                "args": [page_identifier],
            }
            async with session.post(
                endpoint, json=links_payload, headers=headers
            ) as response:
                links = []
                if response.status == 200:
                    try:
                        links = await response.json() or []
                    except Exception:
                        links = []

            # Get page info
            page_info = blocks[0].get("page", {}) if blocks else {}
            page_name = page_info.get(
                "name", page_info.get("originalName", page_identifier)
            )

            # Build comprehensive content-focused output
            output_lines = [
                f"📖 **{page_name}**",
                f"📊 {len(blocks)} blocks | {len(links)} linked sources",
                "",
                "📄 **COMPREHENSIVE CONTENT:**",
                "",
            ]

            # Format all blocks with deep content extraction
            for block in blocks:
                output_lines.extend(format_block_with_content(block, 0, max_depth=6))

            # Add linked references with cleaner format - ALWAYS process all references
            if links:
                output_lines.extend(["🔗 **LINKED REFERENCES:**", ""])

                for i, link_group in enumerate(links[:8], 1):  # Show max 8 sources
                    if isinstance(link_group, list) and len(link_group) >= 1:
                        page_info = link_group[0]
                        if isinstance(page_info, dict):
                            name = page_info.get("name", "Unknown")
                            content_blocks = (
                                link_group[1:] if len(link_group) > 1 else []
                            )

                            # Page type emoji based on content patterns - default to 📖 if no match
                            name_lower = name.lower()
                            emoji = "📖"  # Default emoji for all pages

                            # Try to detect specific patterns, but always use default if no match
                            if any(
                                month in name_lower
                                for month in [
                                    "jan",
                                    "feb",
                                    "mar",
                                    "apr",
                                    "may",
                                    "jun",
                                    "jul",
                                    "aug",
                                    "sep",
                                    "oct",
                                    "nov",
                                    "dec",
                                ]
                            ):
                                emoji = "📅"
                            elif any(
                                word in name_lower
                                for word in [
                                    "class",
                                    "lesson",
                                    "course",
                                    "lecture",
                                    "tutorial",
                                ]
                            ):
                                emoji = "🎓"
                            # else: keep default 📖

                            # ALWAYS display the reference, regardless of pattern matching
                            output_lines.append(
                                f"{emoji} **{name}** ({len(content_blocks)} refs)"
                            )

                            # Show meaningful content previews - ALWAYS process all content blocks
                            for j, block in enumerate(
                                content_blocks[:3]
                            ):  # Max 3 per source
                                if isinstance(block, dict):
                                    content = block.get("content", "")
                                    if "#card" in content:
                                        formatted_card = format_flashcard_content(
                                            content
                                        )
                                        output_lines.append(f"   💡 {formatted_card}")
                                    else:
                                        preview = get_content_preview(
                                            content, 200
                                        )  # Increased preview
                                        if preview != "[No content]":
                                            ref_emoji = (
                                                "📑"
                                                if content.startswith("#")
                                                else "💻"
                                                if "```" in content
                                                else "•"
                                            )
                                            output_lines.append(
                                                f"   {ref_emoji} {preview}"
                                            )
                                        # ALWAYS show something, even if just a placeholder
                                        else:
                                            output_lines.append(
                                                "   • [Referenced content]"
                                            )

                            if len(content_blocks) > 3:
                                output_lines.append(
                                    f"   ... {len(content_blocks) - 3} more references"
                                )

                            output_lines.append("")

                if len(links) > 8:
                    output_lines.append(f"... and {len(links) - 8} more linked sources")
            else:
                output_lines.extend(
                    ["🔗 **LINKED REFERENCES:**", "No linked references found", ""]
                )

            return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [
                TextContent(
                    type="text", text=f"❌ Error getting page content: {str(e)}"
                )
            ]
