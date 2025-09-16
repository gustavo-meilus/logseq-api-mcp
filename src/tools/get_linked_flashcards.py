import os
from pathlib import Path
from typing import Any, List

import aiohttp
from dotenv import load_dotenv
from mcp.types import TextContent

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


async def get_linked_flashcards(page_identifier: str) -> List[TextContent]:
    """
    Get flashcards from the specified page and all pages that link to it.

    Retrieves blocks from the target page and all linked pages, identifies
    flashcard blocks by #card tag, and extracts questions and answers with
    comprehensive metadata.

    Args:
        page_identifier: The name or UUID of the page to search flashcards from
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")

    headers = {"Authorization": f"Bearer {token}"}

    def extract_flashcard_content(content):
        """Extract question and answer parts from flashcard content"""
        if "#card" not in content:
            return None, None

        # Remove #card tag and clean up
        clean_content = content.replace("#card", "").strip()

        # Split by newlines to separate question from options
        lines = clean_content.split("\n")
        if not lines:
            return clean_content, None

        # First line is usually the question
        question = lines[0].strip()

        # Remaining lines might be multiple choice options
        options = []
        for line in lines[1:]:
            line = line.strip()
            if line and (
                line.startswith("+ [")
                or line.startswith("- [")
                or line.startswith("  + [")
                or line.startswith("  - [")
            ):
                options.append(line)

        # Combine question with options if present
        if options:
            full_question = question + "\n" + "\n".join(options)
        else:
            full_question = question

        return full_question, None

    def format_properties_display(props):
        """Format properties for display"""
        if not props:
            return "None"

        formatted_props = []
        for prop_key, value in props.items():
            if (
                prop_key
                not in [
                    "collapsed",
                    "card-last-interval",
                    "card-repeats",
                    "card-ease-factor",
                ]
                and value
            ):
                if isinstance(value, list):
                    value_str = ", ".join(str(v) for v in value)
                else:
                    value_str = str(value)
                formatted_props.append(f"{prop_key}: {value_str}")

        return " | ".join(formatted_props[:3]) if formatted_props else "None"

    async def get_page_blocks(session, page_id):
        """Get blocks for a specific page"""
        payload = {"method": "logseq.Editor.getPageBlocksTree", "args": [page_id]}

        async with session.post(endpoint, json=payload, headers=headers) as response:
            if response.status == 200:
                return await response.json() or []
            return []

    async def get_block_by_uuid(session, block_uuid):
        """Get a specific block by UUID"""
        payload = {"method": "logseq.Editor.getBlock", "args": [block_uuid]}

        async with session.post(endpoint, json=payload, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return None

    def find_flashcards_in_blocks(blocks, page_info):
        """Recursively find flashcard blocks in a block tree"""
        flashcards = []

        def search_blocks(block_list, page_data):
            for block in block_list:
                if isinstance(block, dict):
                    content = block.get("content", "")

                    # Check if this block is a flashcard
                    if "#card" in content:
                        flashcard_data = {
                            "block_id": block.get("id"),
                            "block_uuid": block.get("uuid"),
                            "content": content,
                            "properties": block.get("properties", {}),
                            "children": block.get("children", []),
                            "page": page_data,
                        }
                        flashcards.append(flashcard_data)

                    # Recursively search children
                    children = block.get("children", [])
                    if children:
                        search_blocks(children, page_data)

        search_blocks(blocks, page_info)
        return flashcards

    async with aiohttp.ClientSession() as session:
        try:
            # 1. Get page linked references to find all related pages
            links_payload = {
                "method": "logseq.Editor.getPageLinkedReferences",
                "args": [page_identifier],
            }

            async with session.post(
                endpoint, json=links_payload, headers=headers
            ) as response:
                linked_refs: list[dict[str, Any]] = []
                if response.status == 200:
                    try:
                        linked_refs = await response.json() or []
                    except Exception:
                        linked_refs = []

            # 2. Get all pages for metadata
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

            # 3. Create page lookup and collect page IDs to search
            page_lookup = {}
            for page in all_pages:
                if isinstance(page, dict):
                    page_id = page.get("id")
                    page_name = page.get("name", "").lower()
                    page_original = page.get("originalName", "").lower()

                    if page_id:
                        page_lookup[page_id] = page
                        page_lookup[page_name] = page
                        page_lookup[page_original] = page

            # Find target page
            target_page = None
            search_identifier = page_identifier.lower()
            if search_identifier in page_lookup:
                target_page = page_lookup[search_identifier]

            if not target_page:
                return [
                    TextContent(
                        type="text",
                        text=f"❌ Target page '{page_identifier}' not found",
                    )
                ]

            # 4. Collect all pages to search (target + linked pages)
            pages_to_search = [target_page]

            # Add linked pages
            for link_group in linked_refs:
                if isinstance(link_group, list) and len(link_group) >= 1:
                    page_ref = link_group[0]
                    if isinstance(page_ref, dict):
                        page_id = page_ref.get("id")
                        if page_id and page_id in page_lookup:
                            pages_to_search.append(page_lookup[page_id])

            # 5. Get blocks from all pages and find flashcards
            all_flashcards = []

            for page in pages_to_search:
                page_blocks = await get_page_blocks(
                    session, page.get("name") or page.get("id")
                )
                if page_blocks:
                    page_flashcards = find_flashcards_in_blocks(page_blocks, page)
                    all_flashcards.extend(page_flashcards)

            if not all_flashcards:
                return [
                    TextContent(
                        type="text",
                        text=f"✅ No flashcards found in '{page_identifier}' or its linked pages",
                    )
                ]

            # 6. Enrich flashcards with children (answers)
            enriched_flashcards = []

            for flashcard in all_flashcards:
                # Extract question
                question, _ = extract_flashcard_content(flashcard["content"])

                # Get children (answers)
                children = flashcard["children"]
                answers = []

                for child in children:
                    if (
                        isinstance(child, list)
                        and len(child) >= 2
                        and child[0] == "uuid"
                    ):
                        child_uuid = child[1]
                        child_block = await get_block_by_uuid(session, child_uuid)
                        if child_block:
                            answer_content = child_block.get("content", "").strip()
                            if answer_content:
                                answers.append(
                                    {
                                        "content": answer_content,
                                        "block_id": child_block.get("id"),
                                        "block_uuid": child_block.get("uuid"),
                                    }
                                )

                enriched_flashcard = {
                    "question": question,
                    "answers": answers,
                    "properties": flashcard["properties"],
                    "block_id": flashcard["block_id"],
                    "block_uuid": flashcard["block_uuid"],
                    "page": {
                        "name": flashcard["page"].get("originalName")
                        or flashcard["page"].get("name"),
                        "id": flashcard["page"].get("id"),
                        "uuid": flashcard["page"].get("uuid"),
                    },
                }
                enriched_flashcards.append(enriched_flashcard)

            # 7. Sort flashcards by page name, then by block ID
            enriched_flashcards.sort(
                key=lambda flashcard: (
                    flashcard["page"]["name"] or "",
                    flashcard["block_id"] or 0,
                )
            )

            # 8. Build output
            target_page_name = target_page.get("originalName") or target_page.get(
                "name"
            )

            output_lines = [
                "🎯 **LINKED FLASHCARDS ANALYSIS**",
                f"📄 Target Page: {target_page_name}",
                f"🔗 Searched {len(pages_to_search)} pages (target + {len(pages_to_search) - 1} linked)",
                f"💡 Found {len(enriched_flashcards)} flashcards total",
                "",
                "🧠 **FLASHCARDS:**",
                "",
            ]

            # Group flashcards by page
            flashcards_by_page: dict[str, list[dict[str, Any]]] = {}
            for flashcard in enriched_flashcards:
                page_name = flashcard["page"]["name"]
                if page_name not in flashcards_by_page:
                    flashcards_by_page[page_name] = []
                flashcards_by_page[page_name].append(flashcard)

            for page_name, page_flashcards in flashcards_by_page.items():
                output_lines.extend(
                    [f"📚 **{page_name}** ({len(page_flashcards)} flashcards)", ""]
                )

                for i, flashcard in enumerate(page_flashcards, 1):
                    # Question
                    output_lines.extend(
                        [
                            f"💡 **Flashcard {i}**",
                            f"   🔑 Block ID: {flashcard['block_id']} | UUID: {flashcard['block_uuid']}",
                            f"   📄 Page: {flashcard['page']['name']} (ID: {flashcard['page']['id']})",
                        ]
                    )

                    # Properties
                    props_display = format_properties_display(flashcard["properties"])
                    if props_display != "None":
                        output_lines.append(f"   ⚙️ Properties: {props_display}")

                    # Question
                    output_lines.extend(
                        ["", "   ❓ **QUESTION:**", f"   {flashcard['question']}", ""]
                    )

                    # Answers
                    if flashcard["answers"]:
                        output_lines.append("   💡 **ANSWERS:**")
                        for j, answer in enumerate(flashcard["answers"], 1):
                            output_lines.extend(
                                [
                                    f"   {j}. {answer['content']}",
                                    f"      └─ Block ID: {answer['block_id']} | UUID: {answer['block_uuid']}",
                                ]
                            )
                    else:
                        output_lines.append("   💡 **ANSWERS:** No answer blocks found")

                    output_lines.append("")

            # 9. Add summary
            total_answers = sum(len(f["answers"]) for f in enriched_flashcards)

            output_lines.extend(
                [
                    "📊 **SUMMARY:**",
                    f"• Total flashcards: {len(enriched_flashcards)}",
                    f"• Total answer blocks: {total_answers}",
                    f"• Pages with flashcards: {len(flashcards_by_page)}",
                    f"• Average answers per flashcard: {total_answers / len(enriched_flashcards):.1f}"
                    if enriched_flashcards
                    else "• Average answers per flashcard: 0",
                    "",
                ]
            )

            return [TextContent(type="text", text="\n".join(output_lines))]

        except Exception as e:
            return [
                TextContent(
                    type="text", text=f"❌ Error fetching linked flashcards: {str(e)}"
                )
            ]
