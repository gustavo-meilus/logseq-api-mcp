"""Pytest configuration and shared fixtures."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.client.config import LogseqConfig


# ── Legacy fixtures (kept for compatibility) ─────────────────────────────────


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(
        os.environ,
        {
            "LOGSEQ_API_ENDPOINT": "http://test-logseq:12315/api",
            "LOGSEQ_API_TOKEN": "test-token",
        },
    ):
        yield


@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp ClientSession."""
    with patch("aiohttp.ClientSession") as mock_session_class:
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__aenter__ = AsyncMock(
            return_value=mock_session_instance
        )
        mock_session_class.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_post_context = MagicMock()
        mock_session_instance.post.return_value = mock_post_context
        mock_session_class._session_instance = mock_session_instance
        mock_session_class._post_context = mock_post_context
        yield mock_session_class


@pytest.fixture
def mock_successful_response():
    """Mock successful HTTP response."""
    response = MagicMock()
    response.status = 200
    response.json = AsyncMock(return_value={"success": True, "data": "test data"})
    return response


@pytest.fixture
def mock_error_response():
    """Mock error HTTP response."""
    response = MagicMock()
    response.status = 500
    response.json = AsyncMock(return_value={"error": "Internal server error"})
    return response


@pytest.fixture
def sample_page_data():
    """Sample page data for testing."""
    return {
        "id": 123,
        "uuid": "page-uuid-123",
        "originalName": "Test Page",
        "name": "Test Page",
        "journal?": False,
        "createdAt": 1640995200000,
        "updatedAt": 1640995200000,
    }


@pytest.fixture
def sample_block_data():
    """Sample block data for testing."""
    return {
        "id": 456,
        "uuid": "block-uuid-456",
        "content": "Test block content",
        "level": 1,
        "page": {"id": 123, "name": "Test Page"},
        "properties": {"status": "active"},
        "children": [],
    }


# ── New fixtures: FakeLogseqClient ────────────────────────────────────────────


class FakeLogseqClient:
    """In-memory test double for LogseqClient.

    No HTTP, no aiohttp — pure dict responses.
    Call records are stored in self.calls for assertion.

    Args:
        responses: Dict mapping method name → return value.
    """

    def __init__(self, responses: dict | None = None):
        self.responses = responses or {}
        self.calls: list[tuple[str, tuple, dict]] = []

    # ── Page read ─────────────────────────────────────────────────────────────

    async def get_all_pages(self) -> list[dict]:
        self.calls.append(("get_all_pages", (), {}))
        return self.responses.get("get_all_pages", [])

    async def get_page(self, page_name: str) -> dict | None:
        self.calls.append(("get_page", (page_name,), {}))
        return self.responses.get("get_page")

    async def get_page_blocks_tree(self, page_identifier: str) -> list[dict]:
        self.calls.append(("get_page_blocks_tree", (page_identifier,), {}))
        return self.responses.get("get_page_blocks_tree", [])

    async def get_page_linked_references(self, page_name: str) -> list:
        self.calls.append(("get_page_linked_references", (page_name,), {}))
        return self.responses.get("get_page_linked_references", [])

    async def get_pages_from_namespace(self, namespace: str) -> list[dict]:
        self.calls.append(("get_pages_from_namespace", (namespace,), {}))
        return self.responses.get("get_pages_from_namespace", [])

    async def get_pages_tree_from_namespace(self, namespace: str) -> list[dict]:
        self.calls.append(("get_pages_tree_from_namespace", (namespace,), {}))
        return self.responses.get("get_pages_tree_from_namespace", [])

    # ── Page write ────────────────────────────────────────────────────────────

    async def create_page(self, title: str, properties=None, fmt=None) -> dict:
        self.calls.append(
            ("create_page", (title,), {"properties": properties, "fmt": fmt})
        )
        return self.responses.get(
            "create_page", {"id": 1, "uuid": "new-uuid", "originalName": title}
        )

    async def delete_page(self, page_name: str) -> None:
        self.calls.append(("delete_page", (page_name,), {}))

    async def rename_page(self, old_name: str, new_name: str) -> None:
        self.calls.append(("rename_page", (old_name, new_name), {}))

    async def set_page_properties(self, page_name: str, properties: dict) -> None:
        self.calls.append(
            ("set_page_properties", (page_name,), {"properties": properties})
        )

    # ── Block read ────────────────────────────────────────────────────────────

    async def get_block(
        self, block_uuid: str, include_children: bool = True
    ) -> dict | None:
        self.calls.append(
            ("get_block", (block_uuid,), {"include_children": include_children})
        )
        return self.responses.get("get_block")

    # ── Block write ───────────────────────────────────────────────────────────

    async def append_block_in_page(
        self, page_identifier: str, content: str, options=None
    ) -> dict:
        self.calls.append(("append_block_in_page", (page_identifier, content), {}))
        return self.responses.get("append_block_in_page", {"uuid": "new-block-uuid"})

    async def insert_block(
        self, parent_uuid: str, content: str, properties=None, sibling: bool = False
    ) -> dict:
        self.calls.append(
            ("insert_block", (parent_uuid, content), {"sibling": sibling})
        )
        return self.responses.get("insert_block", {"uuid": "inserted-uuid"})

    async def insert_batch_block(
        self, src_block_uuid: str, blocks: list, sibling: bool = True
    ) -> list:
        self.calls.append(("insert_batch_block", (src_block_uuid,), {"blocks": blocks}))
        return self.responses.get("insert_batch_block", [])

    async def update_block(self, block_uuid: str, content: str) -> None:
        self.calls.append(("update_block", (block_uuid, content), {}))

    async def delete_block(self, block_uuid: str) -> None:
        self.calls.append(("delete_block", (block_uuid,), {}))

    async def upsert_block_property(
        self, block_uuid: str, key: str, value: object
    ) -> None:
        self.calls.append(("upsert_block_property", (block_uuid, key, value), {}))

    async def edit_block(
        self,
        block_uuid: str,
        content=None,
        properties=None,
        cursor_pos=None,
        focus=None,
    ) -> dict:
        self.calls.append(("edit_block", (block_uuid,), {"content": content}))
        return self.responses.get("edit_block", {"uuid": block_uuid})

    # ── Search & Query ────────────────────────────────────────────────────────

    async def search(self, query: str, options=None) -> dict:
        self.calls.append(("search", (query,), {}))
        return self.responses.get("search", {})

    async def query_dsl(self, query: str) -> list[dict]:
        self.calls.append(("query_dsl", (query,), {}))
        return self.responses.get("query_dsl", [])

    # ── DB-mode ───────────────────────────────────────────────────────────────

    async def datascript_query(self, query: str) -> list:
        self.calls.append(("datascript_query", (query,), {}))
        return self.responses.get("datascript_query", [])

    async def resolve_page_uuids(self, uuids: list[str]) -> dict[str, str]:
        self.calls.append(("resolve_page_uuids", (uuids,), {}))
        return self.responses.get("resolve_page_uuids", {})

    async def get_blocks_db_properties(self, blocks: list[dict]) -> dict[str, dict]:
        self.calls.append(("get_blocks_db_properties", (blocks,), {}))
        return self.responses.get("get_blocks_db_properties", {})

    async def resolve_property_ident(self, property_name: str) -> str | None:
        self.calls.append(("resolve_property_ident", (property_name,), {}))
        return self.responses.get("resolve_property_ident")

    async def excluded_page_names(self, ttl_seconds: float = 60.0) -> frozenset[str]:
        self.calls.append(("excluded_page_names", (), {"ttl_seconds": ttl_seconds}))
        return self.responses.get("excluded_page_names", frozenset())

    # ── Live context ──────────────────────────────────────────────────────────

    async def get_current_page(self) -> dict | None:
        self.calls.append(("get_current_page", (), {}))
        return self.responses.get("get_current_page")

    async def get_current_block(self) -> dict | None:
        self.calls.append(("get_current_block", (), {}))
        return self.responses.get("get_current_block")

    async def get_editing_selection(self) -> list[dict]:
        self.calls.append(("get_editing_selection", (), {}))
        return self.responses.get("get_editing_selection", [])

    async def get_current_graph(self) -> dict:
        self.calls.append(("get_current_graph", (), {}))
        return self.responses.get("get_current_graph", {})


@pytest.fixture
def fake_client():
    """Return a fresh FakeLogseqClient with no preset responses."""
    return FakeLogseqClient()


@pytest.fixture
def config():
    """Return a standard test LogseqConfig."""
    return LogseqConfig(endpoint="http://test:12315/api", token="test-token")
