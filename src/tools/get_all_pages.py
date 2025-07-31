import os
import aiohttp
from typing import List
from mcp.types import TextContent
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def get_all_pages(start: int = None, end: int = None) -> List[TextContent]:
    """
    Get a simple list of all pages in the Logseq graph with essential metadata.

    Returns a clean listing optimized for LLM consumption with key identifiers
    and timestamps for each page. By default shows all pages, but can be limited
    with start and end parameters.
    
    Args:
        start: Starting index (0-based, inclusive). If None, starts from beginning.
        end: Ending index (0-based, exclusive). If None, goes to end.
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    def format_timestamp(timestamp):
        """Convert timestamp to readable format"""
        if not timestamp:
            return "N/A"
        try:
            from datetime import datetime

            dt = datetime.fromtimestamp(timestamp / 1000)  # Convert from ms
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError, OverflowError):
            return str(timestamp)

    def format_page_entry(page):
        """Format a single page entry with essential metadata"""
        page_id = page.get("id", "N/A")
        uuid = page.get("uuid", "N/A")
        original_name = page.get("originalName", page.get("name", "Unknown"))
        created_at = format_timestamp(page.get("createdAt"))
        updated_at = format_timestamp(page.get("updatedAt"))

        # Determine page type
        page_type = "📅 Journal" if page.get("journal?", False) else "📄 Page"

        return f"{page_type} **{original_name}** | ID: {page_id} | UUID: {uuid} | Created: {created_at} | Updated: {updated_at}"

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

            # Sort pages alphabetically by name
            sorted_pages = sorted(
                pages, key=lambda p: p.get("originalName", p.get("name", "")).lower()
            )

            # Separate journal and regular pages
            journal_pages = [p for p in sorted_pages if p.get("journal?", False)]
            regular_pages = [p for p in sorted_pages if not p.get("journal?", False)]

            # Apply start/end limits if specified
            if start is not None or end is not None:
                # Apply limits to regular pages
                regular_pages = regular_pages[start:end]
                # Apply limits to journal pages  
                journal_pages = journal_pages[start:end]
                
                # Build output with range information
                range_info = f" (showing indices {start if start is not None else 0}-{end if end is not None else 'end'})"
                output_lines = [
                    f"📊 **LOGSEQ PAGES LISTING{range_info}**",
                    f"📈 Total pages in graph: {len(pages)}",
                    f"📄 Regular pages shown: {len(regular_pages)}",
                    f"📅 Journal pages shown: {len(journal_pages)}",
                    "",
                ]
            else:
                # Build simple output with clear distinction between Journal and Regular pages
                output_lines = [
                    "📊 **LOGSEQ PAGES LISTING**",
                    f"📈 Total pages: {len(pages)}",
                    f"📅 Journal pages: {len(journal_pages)}",
                    f"📄 Regular pages: {len(regular_pages)}",
                    "",
                ]

            # Add regular pages section
            if regular_pages:
                output_lines.extend(["📄 **REGULAR PAGES:**", ""])
                for page in regular_pages:
                    output_lines.append(
                        format_page_entry(page).replace("📄 Page", "📄")
                    )

            # Add journal pages section
            if journal_pages:
                output_lines.extend(["", "📅 **JOURNAL PAGES:**", ""])
                for page in journal_pages:
                    output_lines.append(
                        format_page_entry(page).replace("📅 Journal", "📅")
                    )

            return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error fetching pages: {str(e)}")]
