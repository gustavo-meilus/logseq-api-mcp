"""Async HTTP client for the Logseq local API."""

import asyncio
import time
from typing import Any

import aiohttp

from .config import LogseqConfig
from .exceptions import (
    LogseqAPIError,
    LogseqAuthError,
    LogseqConnectionError,
    LogseqNotFoundError,
)


async def _interpret(response: aiohttp.ClientResponse, method: str) -> Any:
    """Translate an aiohttp response into a value or a typed exception.

    @param response aiohttp response object (already awaited as context manager).
    @param method   The logseq method called, used for error messages.
    @returns        Parsed JSON body when status == 200.
    @throws LogseqAuthError, LogseqNotFoundError, LogseqAPIError.
    @complexity O(1).
    """
    status = response.status
    if status == 200:
        try:
            return await response.json()
        except Exception:
            return await response.text()
    if status == 401:
        raise LogseqAuthError(f"Auth failed calling {method}", status_code=401)
    if status == 404:
        raise LogseqNotFoundError(f"Unknown method {method}", status_code=404)
    body = await response.text()
    raise LogseqAPIError(
        f"HTTP {status} from {method}: {body[:200]}", status_code=status
    )


class LogseqClient:
    """Async HTTP client for the Logseq local API.

    All methods correspond 1:1 to Logseq Editor/DB API calls.
    Constructed with an injected LogseqConfig; never reads env vars.

    Args:
        config: Immutable configuration object.

    Complexity: O(1) construction.
    """

    def __init__(self, config: LogseqConfig) -> None:
        self._config = config
        self._excluded_cache: tuple[float, frozenset[str]] | None = None

    # ── Internal ─────────────────────────────────────────────────────────────

    async def _call(self, method: str, args: list | None = None) -> Any:
        """Issue a JSON-RPC POST to /api and map HTTP status to typed exceptions.

        @param method  Logseq method name, e.g. "logseq.Editor.getAllPages".
        @param args    Positional args list forwarded as JSON; defaults to [].
        @returns       Parsed JSON response body.
        @throws LogseqAuthError       on HTTP 401.
        @throws LogseqNotFoundError   on HTTP 404.
        @throws LogseqAPIError        on any other 4xx/5xx with status_code set.
        @throws LogseqConnectionError on aiohttp connector errors and asyncio timeouts.
        @complexity O(1) network call.
        """
        payload = {"method": method, "args": args or []}
        headers = {
            "Authorization": f"Bearer {self._config.token}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self._config.endpoint,
                    json=payload,
                    headers=headers,
                    ssl=self._config.verify_ssl,
                ) as response:
                    return await _interpret(response, method)
        except (aiohttp.ClientConnectorError, asyncio.TimeoutError) as exc:
            raise LogseqConnectionError(
                f"Cannot reach Logseq API at {self._config.endpoint}: {exc}"
            ) from exc

    # ── Page read operations ──────────────────────────────────────────────────

    async def get_all_pages(self) -> list[dict]:
        """Return all pages in the Logseq graph.

        Returns:
            List of page dicts. Empty list if API returns None.

        Complexity: O(N) where N is page count.
        """
        result = await self._call("logseq.Editor.getAllPages")
        return result if result is not None else []

    async def get_page(self, page_name: str) -> dict | None:
        """Return a single page by name.

        Args:
            page_name: Exact page name.

        Returns:
            Page dict, or None if not found.

        Complexity: O(1).
        """
        return await self._call("logseq.Editor.getPage", [page_name])

    async def get_page_blocks_tree(self, page_identifier: str) -> list[dict]:
        """Return the block tree for a page.

        Args:
            page_identifier: Page name or UUID.

        Returns:
            List of top-level block dicts with nested children.

        Complexity: O(N) where N is block count.
        """
        result = await self._call("logseq.Editor.getPageBlocksTree", [page_identifier])
        return result if result is not None else []

    async def get_page_linked_references(self, page_name: str) -> list:
        """Return backlinks for a page.

        Args:
            page_name: Exact page name.

        Returns:
            List of [page_info, blocks] pairs.

        Complexity: O(R) where R is reference count.
        """
        result = await self._call("logseq.Editor.getPageLinkedReferences", [page_name])
        return result if result is not None else []

    async def get_pages_from_namespace(self, namespace: str) -> list[dict]:
        """Return a flat list of pages within a namespace.

        Args:
            namespace: Namespace prefix (e.g. 'Projects').

        Returns:
            List of page dicts.

        Complexity: O(N).
        """
        result = await self._call("logseq.Editor.getPagesFromNamespace", [namespace])
        return result if result is not None else []

    async def get_pages_tree_from_namespace(self, namespace: str) -> list[dict]:
        """Return a nested page tree for a namespace.

        Args:
            namespace: Root namespace (e.g. 'Projects').

        Returns:
            Nested list of page dicts with 'children' keys.

        Complexity: O(N).
        """
        result = await self._call(
            "logseq.Editor.getPagesTreeFromNamespace", [namespace]
        )
        return result if result is not None else []

    async def excluded_page_names(self, ttl_seconds: float = 60.0) -> frozenset[str]:
        """Return the lower-cased set of page names hidden by exclude_tags, cached.

        @param ttl_seconds Cache lifetime; reuse last result if younger than ttl.
        @returns           frozenset of lower-cased originalName values.
        @complexity        O(N) on cache miss for N pages; O(1) on hit.
        """
        if not self._config.exclude_tags:
            return frozenset()
        now = time.monotonic()
        if self._excluded_cache is not None:
            cached_at, cached = self._excluded_cache
            if now - cached_at < ttl_seconds:
                return cached
        from src.privacy.exclude_tags import (
            extract_tags,  # local import to avoid cycle
            is_page_excluded,  # local import to avoid cycle
        )

        pages = await self.get_all_pages()
        lowered_excludes = tuple(t.lower() for t in self._config.exclude_tags)

        def _excluded(page: dict) -> bool:
            # Normalize page tags to lower-case so comparison is case-insensitive
            # even before E1 lands case-insensitive support in is_page_excluded.
            props = page.get("properties") or {}
            lowered = [str(t).lower() for t in extract_tags(props)]
            return is_page_excluded({"properties": {"tags": lowered}}, lowered_excludes)

        excluded = frozenset(
            str(p.get("originalName", "")).lower() for p in pages if _excluded(p)
        )
        self._excluded_cache = (time.monotonic(), excluded)
        return excluded

    # ── Page write operations ─────────────────────────────────────────────────

    async def create_page(
        self,
        title: str,
        properties: dict | None = None,
        fmt: str | None = None,
    ) -> dict:
        """Create a new Logseq page.

        @param title      Page title (used as PageIdentity).
        @param properties Optional bare properties dict (NOT nested under opts).
        @param fmt        Optional format string ('markdown' | 'org'); becomes opts.format.
        @returns          Created PageEntity dict (or empty dict if API returns null).
        @throws LogseqAPIError on backend failure.
        @complexity O(1) network call.
        """
        opts: dict = {}
        if fmt:
            opts["format"] = fmt
        result = await self._call(
            "logseq.Editor.createPage",
            [title, properties or {}, opts],
        )
        return result or {}

    async def delete_page(self, page_name: str) -> None:
        """Delete a page by name.

        Args:
            page_name: Exact page name to delete.

        Complexity: O(1).
        """
        await self._call("logseq.Editor.deletePage", [page_name])

    async def rename_page(self, old_name: str, new_name: str) -> None:
        """Rename a page and update all references.

        Args:
            old_name: Current page name.
            new_name: New page name.

        Complexity: O(R) where R is reference count.
        """
        await self._call("logseq.Editor.renamePage", [old_name, new_name])

    async def set_page_properties(self, page_name: str, properties: dict) -> None:
        """Set page-level properties.

        Args:
            page_name: Exact page name.
            properties: Dict of property key/value pairs.

        Complexity: O(P) where P is property count.
        """
        await self._call("logseq.Editor.setPageProperties", [page_name, properties])

    # ── Block read operations ─────────────────────────────────────────────────

    async def get_block(
        self, block_uuid: str, include_children: bool = True
    ) -> dict | None:
        """Return a single block by UUID.

        Args:
            block_uuid: Block UUID string.
            include_children: Whether to recursively include child blocks.

        Returns:
            Block dict with optional children, or None if not found.

        Complexity: O(N) where N is descendant count when include_children=True.
        """
        options = {"includeChildren": include_children}
        return await self._call("logseq.Editor.getBlock", [block_uuid, options])

    # ── Block write operations ────────────────────────────────────────────────

    async def append_block_in_page(
        self,
        page_identifier: str,
        content: str,
        options: dict | None = None,
    ) -> dict:
        """Append a block at the bottom of a Logseq page.

        @param page_identifier PageIdentity (name).
        @param content         Markdown block content.
        @param options         Optional opts dict per IEditorProxy (properties=…).
        @returns               BlockEntity dict.
        @throws LogseqAPIError on backend failure.
        @complexity O(1).
        """
        args: list = [page_identifier, content]
        if options is not None:
            args.append(options)
        result = await self._call("logseq.Editor.appendBlockInPage", args)
        return result or {}

    async def insert_block(
        self,
        parent_uuid: str,
        content: str,
        properties: dict | None = None,
        sibling: bool = False,
    ) -> dict:
        """Insert a block as a child or sibling of an existing block.

        Args:
            parent_uuid: UUID of the reference block.
            content: Text content for the new block.
            properties: Optional block properties dict.
            sibling: False = child insertion, True = sibling insertion.

        Returns:
            Created block dict.

        Complexity: O(1).
        """
        options: dict = {"sibling": sibling}
        if properties:
            options["properties"] = properties
        result = await self._call(
            "logseq.Editor.insertBlock", [parent_uuid, content, options]
        )
        return result or {}

    async def insert_batch_block(
        self,
        src_block_uuid: str,
        blocks: list[dict],
        sibling: bool = True,
    ) -> list[dict]:
        """Insert multiple blocks in batch.

        Args:
            src_block_uuid: UUID of the reference block.
            blocks: List of IBatchBlock dicts.
            sibling: Whether to insert as siblings of src_block.

        Returns:
            List of created block dicts.

        Complexity: O(N) where N is block count.
        """
        options = {"sibling": sibling}
        result = await self._call(
            "logseq.Editor.insertBatchBlock", [src_block_uuid, blocks, options]
        )
        return result if result is not None else []

    async def update_block(self, block_uuid: str, content: str) -> None:
        """Replace the content of an existing block.

        Args:
            block_uuid: Block UUID string.
            content: New content string.

        Complexity: O(1).
        """
        await self._call("logseq.Editor.updateBlock", [block_uuid, content])

    async def delete_block(self, block_uuid: str) -> None:
        """Delete a block by UUID.

        Args:
            block_uuid: Block UUID string.

        Complexity: O(1).
        """
        await self._call("logseq.Editor.removeBlock", [block_uuid])

    async def upsert_block_property(
        self, block_uuid: str, key: str, value: object
    ) -> None:
        """Set or update a single property on a block.

        Args:
            block_uuid: Block UUID string.
            key: Property key (internal ident for DB mode).
            value: Property value.

        Complexity: O(1).
        """
        await self._call("logseq.Editor.upsertBlockProperty", [block_uuid, key, value])

    async def edit_block(
        self,
        block_uuid: str,
        content: str | None = None,
        properties: dict | None = None,
        cursor_pos: int | None = None,
        focus: bool | None = None,
    ) -> dict:
        """Open a block in the Logseq editor (sets cursor focus).

        Args:
            block_uuid: Block UUID string.
            content: Optional new content to set.
            properties: Optional properties to set.
            cursor_pos: Optional cursor position.
            focus: Optional focus flag.

        Returns:
            API response dict.

        Complexity: O(1).
        """
        options: dict = {}
        if content is not None:
            options["content"] = content
        if properties is not None:
            options["properties"] = properties
        if cursor_pos is not None:
            options["pos"] = cursor_pos
        if focus is not None:
            options["focus"] = focus
        result = await self._call("logseq.Editor.editBlock", [block_uuid, options])
        return result or {}

    # ── Live context (UI state) ───────────────────────────────────────────────

    async def get_current_page(self) -> dict | None:
        """Return the page currently open in the Logseq editor.

        Returns:
            Page dict, or None if no page is active.

        Complexity: O(1).
        """
        return await self._call("logseq.Editor.getCurrentPage")

    async def get_current_block(self) -> dict | None:
        """Return the block where the cursor is currently positioned.

        Returns:
            Block dict, or None if no block is being edited.

        Complexity: O(1).
        """
        return await self._call("logseq.Editor.getCurrentBlock")

    async def get_editing_selection(self) -> list[dict]:
        """Return the list of blocks currently selected in the editor.

        Returns:
            List of selected block dicts. Empty list if no selection.

        Complexity: O(S) where S is selected block count.
        """
        result = await self._call("logseq.Editor.getEditingBlockSelection")
        return result if result is not None else []

    async def get_current_graph(self) -> dict:
        """Return metadata for the currently active Logseq graph.

        Returns:
            Dict with 'name', 'path', and 'url' keys. Empty dict if unavailable.

        Complexity: O(1).
        """
        result = await self._call("logseq.App.getCurrentGraph")
        return result if result is not None else {}

    # ── Search & Query ────────────────────────────────────────────────────────

    async def search(self, query: str, options: dict | None = None) -> dict:
        """Full-text search across pages and blocks.

        Args:
            query: Search query string.
            options: Optional search options dict (e.g. {'limit': 20}).

        Returns:
            Search result dict with 'blocks', 'pages', 'files' keys.

        Complexity: O(N) where N is matching content count.
        """
        result = await self._call("logseq.App.search", [query, options or {}])
        return result if result is not None else {}

    async def query_dsl(self, query: str) -> list[dict]:
        """Execute a Logseq DSL query.

        Args:
            query: Logseq DSL query string (e.g. '(page-property status active)').

        Returns:
            List of matching page or block dicts.

        Complexity: O(N) where N is result count.
        """
        result = await self._call("logseq.DB.q", [query])
        return result if result is not None else []

    # ── DB-mode operations ────────────────────────────────────────────────────

    async def datascript_query(self, query: str) -> list:
        """Execute a raw Datascript query.

        Args:
            query: Datascript query string.

        Returns:
            List of result tuples or dicts.

        Complexity: O(N) where N is result count.
        """
        result = await self._call("logseq.DB.datascriptQuery", [query])
        return result if result is not None else []

    async def resolve_page_uuids(self, uuids: list[str]) -> dict[str, str]:
        """Resolve a batch of page UUIDs to their original names in one query.

        @complexity O(1) network call (single datascript) + O(R) for R rows.
        """
        if not uuids:
            return {}
        safe = [u.replace("\\", "\\\\").replace('"', '\\"') for u in uuids]
        or_clauses = " ".join(f'[?e :block/uuid "{u}"]' for u in safe)
        query = (
            "[:find ?uuid ?name "
            ":where "
            f"(or {or_clauses}) "
            "[?e :block/uuid ?uuid] "
            "[?e :block/original-name ?name]]"
        )
        rows = await self.datascript_query(query)
        return {
            row[0]: row[1] for row in rows if isinstance(row, list) and len(row) >= 2
        }

    async def get_blocks_db_properties(self, blocks: list[dict]) -> dict[str, dict]:
        """Fetch DB-mode properties for a list of blocks.

        Args:
            blocks: List of block dicts with 'uuid' keys.

        Returns:
            Dict mapping block uuid → {property_key: value}.

        Complexity: O(B) where B is block count.
        """
        result: dict[str, dict] = {}
        for block in blocks:
            uuid = block.get("uuid")
            if not uuid:
                continue
            props = block.get("properties", {})
            if props:
                result[str(uuid)] = {
                    k: v for k, v in props.items() if not str(k).startswith(":logseq")
                }
        return result

    async def resolve_property_ident(self, property_name: str) -> str | None:
        """Resolve a property display name to its DB-mode :db/ident keyword.

        @param property_name User-facing property name (e.g. "status").
        @returns             ":db/ident" string (e.g. ":user.property/status") or None when unknown.
        @complexity O(1) network call.
        """
        safe = property_name.replace("\\", "\\\\").replace('"', '\\"')
        query = (
            f'[:find ?ident :where [?e :block/title "{safe}"] [?e :db/ident ?ident]]'
        )
        rows = await self.datascript_query(query)
        if not rows:
            return None
        first = rows[0]
        if isinstance(first, list) and first:
            return str(first[0])
        return None
