import os
import aiohttp
from typing import List
from mcp.types import TextContent
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def get_all_pages() -> List[TextContent]:
    """
    Get a comprehensive list of all pages in the Logseq graph with key metadata.

    Returns formatted data optimized for LLM consumption with categorization,
    essential properties, and organized structure.
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    def categorize_page(page):
        """Categorize pages based on journal vs regular content"""
        # Journal pages (date-based)
        if page.get("journal?", False):
            return "📅 Journal"

        return "📄 Pages"

    def format_essential_properties(props):
        """Extract and format only the most important properties"""
        if not props:
            return []

        essential = []

        # Educational properties
        if "curso" in props:
            curso = props["curso"]
            if isinstance(curso, list):
                curso = ", ".join(str(c) for c in curso)
            essential.append(f"📚 {curso}")

        if "professor" in props:
            prof = props["professor"]
            if isinstance(prof, list):
                prof = ", ".join(str(p) for p in prof)
            essential.append(f"👨‍🏫 {prof}")

        if "data" in props:
            data = props["data"]
            if isinstance(data, list):
                data = ", ".join(str(d) for d in data)
            essential.append(f"📅 {data}")

        if "tipo" in props:
            tipo = props["tipo"]
            if isinstance(tipo, list):
                tipo = ", ".join(str(t) for t in tipo)
            essential.append(f"🏷️ {tipo}")

        # Technical properties
        if "tecnologias" in props:
            tech = props["tecnologias"]
            if isinstance(tech, list) and tech:
                tech_str = ", ".join(str(t) for t in tech)
                essential.append(f"⚙️ {tech_str}")

        return essential

    def format_page_entry(page, show_details=True):
        """Format a single page entry with essential information"""
        name = page.get("name", "Unknown")
        original_name = page.get("originalName", name)
        page_id = page.get("id", "N/A")

        # Basic info line
        display_name = original_name if original_name != name else name
        lines = [f"📄 **{display_name}** [ID: {page_id}]"]

        if show_details:
            # Essential properties
            properties = page.get("properties", {})
            essential_props = format_essential_properties(properties)
            if essential_props:
                lines.append(f"   {' | '.join(essential_props)}")

            # Additional metadata
            metadata = []
            if page.get("journal?", False):
                metadata.append("📅 Journal")

            created_at = page.get("createdAt")
            updated_at = page.get("updatedAt")
            if updated_at and created_at and updated_at != created_at:
                metadata.append("✏️ Modified")

            if page.get("file"):
                metadata.append("📁 Has file")

            if metadata:
                lines.append(f"   {' | '.join(metadata)}")

        return lines

    async with aiohttp.ClientSession() as session:
        try:
            # Get all pages
            payload = {"method": "logseq.Editor.getAllPages"}

            async with session.post(
                endpoint, json=payload, headers=headers
            ) as response:
                if response.status != 200:
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Failed to fetch pages: HTTP {response.status}",
                        )
                    ]

                pages = await response.json()
                if not pages:
                    return [
                        TextContent(
                            type="text", text="✅ No pages found in Logseq graph"
                        )
                    ]

            # Categorize and organize pages
            categorized_pages = {}
            for page in pages:
                category = categorize_page(page)
                if category not in categorized_pages:
                    categorized_pages[category] = []
                categorized_pages[category].append(page)

            # Build output
            output_lines = [
                "📊 **LOGSEQ GRAPH OVERVIEW**",
                f"📈 Total pages: {len(pages)}",
                f"📅 Journal pages: {len([p for p in pages if p.get('journal?', False)])}",
                f"📄 Regular pages: {len([p for p in pages if not p.get('journal?', False)])}",
                "",
            ]

            # Detailed breakdown by category
            output_lines.append("📚 **DETAILED BREAKDOWN:**")
            output_lines.append("")

            for category, category_pages in sorted(categorized_pages.items()):
                output_lines.append(f"## {category} ({len(category_pages)} pages)")
                output_lines.append("")

                # Sort pages by name for better organization
                sorted_pages = sorted(
                    category_pages,
                    key=lambda p: p.get("originalName", p.get("name", "")),
                )

                # Show all pages for smaller categories, limit for larger ones
                display_pages = sorted_pages
                truncated = False

                if len(sorted_pages) > 50:
                    display_pages = sorted_pages[:25]
                    truncated = True

                for page in display_pages:
                    page_lines = format_page_entry(page, show_details=True)
                    output_lines.extend(page_lines)
                    output_lines.append("")

                if truncated:
                    remaining = len(sorted_pages) - len(display_pages)
                    output_lines.append(
                        f"... and {remaining} more pages in this category"
                    )
                    output_lines.append("")

            # Quick reference index
            output_lines.extend(["🔍 **QUICK REFERENCE INDEX:**", ""])

            all_pages_sorted = sorted(
                pages, key=lambda p: p.get("originalName", p.get("name", ""))
            )
            for page in all_pages_sorted:
                name = page.get("originalName", page.get("name", "Unknown"))
                page_id = page.get("id", "N/A")
                emoji = "📅" if page.get("journal?", False) else "📄"
                output_lines.append(f"{emoji} {name} [ID: {page_id}]")

            return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error fetching pages: {str(e)}")]
