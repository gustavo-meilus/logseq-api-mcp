"""Tests for get_current_block tool."""

from src.client.config import LogseqConfig
from tests.conftest import FakeLogseqClient
from src.tools.get_current_block import get_current_block as _run

_cfg = LogseqConfig("http://x", "t")

_BLOCK = {
    "uuid": "block-uuid-1",
    "content": "This is my current block content",
    "page": {"name": "My Notes", "originalName": "My Notes"},
    "level": 1,
}


class TestGetCurrentBlock:
    async def test_returns_block_content_when_editing(self):
        client = FakeLogseqClient({"get_current_block": _BLOCK})
        result = await _run(client, _cfg)
        assert "This is my current block content" in result[0].text

    async def test_returns_block_uuid_when_editing(self):
        client = FakeLogseqClient({"get_current_block": _BLOCK})
        result = await _run(client, _cfg)
        assert "block-uuid-1" in result[0].text

    async def test_returns_no_active_block_when_none(self):
        client = FakeLogseqClient({"get_current_block": None})
        result = await _run(client, _cfg)
        assert "No active block" in result[0].text

    async def test_returns_error_on_exception(self):
        class ErrorClient(FakeLogseqClient):
            async def get_current_block(self):
                raise RuntimeError("timeout")

        result = await _run(ErrorClient(), _cfg)
        assert "❌" in result[0].text
