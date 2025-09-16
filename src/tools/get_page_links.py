import os
from pathlib import Path
from typing import Any, List

import aiohttp
from dotenv import load_dotenv
from mcp.types import TextContent

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def get_page_links(page_identifier: str) -> List[TextContent]:
    """
    Get pages that link to the specified page with comprehensive metadata.

    Retrieves all pages that reference the target page and enriches them with
    full metadata including creation dates, journal status, and UUIDs.

    Args:
        page_identifier: The name or UUID of the page to find links to
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

    def format_page_entry(page_ref, full_page_data=None):
        """Format a single page entry with complete metadata"""
        # Basic info from reference
        ref_name = page_ref.get("name", "Unknown")
        ref_original_name = page_ref.get("originalName", ref_name)
        ref_id = page_ref.get("id", "N/A")

        # Enhanced info from full page data
        if full_page_data:
            created_at = format_timestamp(full_page_data.get("createdAt"))
            updated_at = format_timestamp(full_page_data.get("updatedAt"))
            is_journal = full_page_data.get("journal?", False)
            uuid = full_page_data.get("uuid", "N/A")

            # Get properties if available
            properties = full_page_data.get("properties", {})

            return {
                "name": ref_name,
                "original_name": ref_original_name,
                "id": ref_id,
                "uuid": uuid,
                "created_at": created_at,
                "updated_at": updated_at,
                "is_journal": is_journal,
                "properties": properties,
            }
        else:
            return {
                "name": ref_name,
                "original_name": ref_original_name,
                "id": ref_id,
                "uuid": "N/A",
                "created_at": "N/A",
                "updated_at": "N/A",
                "is_journal": False,
                "properties": {},
            }

    def format_properties_display(props):
        """Format properties for display"""
        if not props:
            return "None"

        # Show only meaningful properties
        filtered_props = {}
        for property_name, value in props.items():
            if (
                property_name not in ["collapsed", "card-last-interval", "card-repeats"]
                and value
            ):
                if isinstance(value, list):
                    filtered_props[property_name] = ", ".join(str(v) for v in value)
                else:
                    filtered_props[property_name] = str(value)

        if not filtered_props:
            return "None"

        prop_lines = []
        for prop_name, prop_value in list(filtered_props.items())[
            :3
        ]:  # Show top 3 properties
            prop_lines.append(f"  • {prop_name}: {prop_value}")

        return "\n".join(prop_lines)

    async with aiohttp.ClientSession() as session:
        try:
            # 1. Get page linked references
            links_payload = {
                "method": "logseq.Editor.getPageLinkedReferences",
                "args": [page_identifier],
            }

            async with session.post(
                endpoint, json=links_payload, headers=headers
            ) as response:
                if response.status != 200:
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Failed to fetch page links: HTTP {response.status}",
                        )
                    ]

                linked_refs = await response.json()
                if not linked_refs:
                    return [
                        TextContent(
                            type="text", text=f"✅ No pages link to '{page_identifier}'"
                        )
                    ]

            # 2. Get all pages for metadata enrichment
            all_pages_payload = {"method": "logseq.Editor.getAllPages"}

            async with session.post(
                endpoint, json=all_pages_payload, headers=headers
            ) as response:
                all_pages: list[dict[str, Any]] = []
                if response.status == 200:
                    try:
                        all_pages = await response.json() or []
                    except Exception:
                        all_pages = []

            # 3. Extract unique page references from linked references
            unique_pages = {}
            reference_counts = {}

            for link_group in linked_refs:
                if isinstance(link_group, list) and len(link_group) >= 1:
                    page_ref = link_group[0]
                    if isinstance(page_ref, dict):
                        page_id = page_ref.get("id")
                        if page_id:
                            unique_pages[page_id] = page_ref
                            # Count number of references from this page
                            reference_counts[page_id] = len(link_group) - 1

            # 4. Create page lookup by ID for enrichment
            page_lookup = {}
            for page in all_pages:
                if isinstance(page, dict):
                    page_id = page.get("id")
                    if page_id:
                        page_lookup[page_id] = page

            # 5. Build enriched page entries
            enriched_pages = []
            for page_id, page_ref in unique_pages.items():
                full_page_data = page_lookup.get(page_id)
                page_entry = format_page_entry(page_ref, full_page_data)
                page_entry["reference_count"] = reference_counts.get(page_id, 0)
                enriched_pages.append(page_entry)

            # 6. Sort pages by reference count (most references first), then by name
            def sort_pages(page):
                return (-page["reference_count"], page["name"].lower())

            # Sort using a different approach to avoid sort parameter
            page_sorts = [(sort_pages(page), page) for page in enriched_pages]
            page_sorts.sort()
            enriched_pages = [page for _, page in page_sorts]

            # 7. Build output
            output_lines = [
                "🔗 **PAGE LINKS ANALYSIS**",
                f"📄 Target Page: {page_identifier}",
                f"📊 Found {len(enriched_pages)} pages linking to this page",
                f"📈 Total reference groups: {len(linked_refs)}",
                "",
                "🎯 **LINKING PAGES:**",
                "",
            ]

            # Display each linking page
            for i, page in enumerate(enriched_pages, 1):
                emoji = "📅" if page["is_journal"] else "📄"
                display_name = (
                    page["original_name"]
                    if page["original_name"] != page["name"]
                    else page["name"]
                )

                output_lines.extend(
                    [
                        f"{emoji} **{i}. {display_name}**",
                        f"   🔑 ID: {page['id']} | UUID: {page['uuid']}",
                        f"   📊 References: {page['reference_count']} | Journal: {'Yes' if page['is_journal'] else 'No'}",
                        f"   📅 Created: {page['created_at']}",
                        f"   🔄 Updated: {page['updated_at']}",
                    ]
                )

                # Show properties if available
                props_display = format_properties_display(page["properties"])
                if props_display != "None":
                    output_lines.extend(["   ⚙️ Properties:", props_display])

                output_lines.append("")

            # 8. Add summary statistics
            journal_pages = sum(1 for p in enriched_pages if p["is_journal"])
            regular_pages = len(enriched_pages) - journal_pages
            total_refs = sum(p["reference_count"] for p in enriched_pages)

            output_lines.extend(
                [
                    "📈 **SUMMARY:**",
                    f"• Total linking pages: {len(enriched_pages)}",
                    f"• Journal pages: {journal_pages}",
                    f"• Regular pages: {regular_pages}",
                    f"• Total references: {total_refs}",
                    f"• Average references per page: {total_refs / len(enriched_pages):.1f}"
                    if enriched_pages
                    else "• Average references per page: 0",
                    "",
                ]
            )

            return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [
                TextContent(type="text", text=f"❌ Error fetching page links: {str(e)}")
            ]
