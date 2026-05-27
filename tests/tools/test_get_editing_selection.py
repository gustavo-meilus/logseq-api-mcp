"""Tests for get_editing_selection tool."""

from src.client.config import LogseqConfig
from tests.conftest import FakeLogseqClient
from src.tools.get_editing_selection import get_editing_selection as _run

_cfg = LogseqConfig("http://x", "t")

_SELECTION = [
    {"uuid": "b1", "content": "First selected block"},
    {"uuid": "b2", "content": "Second selected block"},
]


class TestGetEditingSelection:
    async def test_returns_selected_blocks_content(self):
        client = FakeLogseqClient({"get_editing_selection": _SELECTION})
        result = await _run(client, _cfg)
        assert "First selected block" in result[0].text
        assert "Second selected block" in result[0].text

    async def test_returns_block_count(self):
        client = FakeLogseqClient({"get_editing_selection": _SELECTION})
        result = await _run(client, _cfg)
        assert "2" in result[0].text

    async def test_returns_no_selection_when_empty(self):
        client = FakeLogseqClient({"get_editing_selection": []})
        result = await _run(client, _cfg)
        assert "No blocks selected" in result[0].text

    async def test_returns_error_on_exception(self):
        class ErrorClient(FakeLogseqClient):
            async def get_editing_selection(self):
                raise RuntimeError("api error")

        result = await _run(ErrorClient(), _cfg)
        assert "❌" in result[0].text
