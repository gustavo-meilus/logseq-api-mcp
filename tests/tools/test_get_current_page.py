"""Tests for get_current_page tool."""

from src.client.config import LogseqConfig
from tests.conftest import FakeLogseqClient
from src.tools.get_current_page import get_current_page as _run

_cfg = LogseqConfig("http://x", "t")

_PAGE = {
    "name": "my-notes",
    "originalName": "My Notes",
    "uuid": "page-uuid-1",
    "journal?": False,
    "updatedAt": 1700000000000,
}


class TestGetCurrentPage:
    async def test_returns_page_name_when_active(self):
        client = FakeLogseqClient({"get_current_page": _PAGE})
        result = await _run(client, _cfg)
        assert "My Notes" in result[0].text

    async def test_returns_page_uuid_when_active(self):
        client = FakeLogseqClient({"get_current_page": _PAGE})
        result = await _run(client, _cfg)
        assert "page-uuid-1" in result[0].text

    async def test_returns_no_active_page_message_when_none(self):
        client = FakeLogseqClient({"get_current_page": None})
        result = await _run(client, _cfg)
        assert "No active page" in result[0].text

    async def test_returns_error_on_exception(self):
        class ErrorClient(FakeLogseqClient):
            async def get_current_page(self):
                raise RuntimeError("connection refused")

        result = await _run(ErrorClient(), _cfg)
        assert "❌" in result[0].text

    async def test_journal_page_indicated(self):
        journal_page = {**_PAGE, "journal?": True, "originalName": "2024-01-15"}
        client = FakeLogseqClient({"get_current_page": journal_page})
        result = await _run(client, _cfg)
        assert "2024-01-15" in result[0].text
