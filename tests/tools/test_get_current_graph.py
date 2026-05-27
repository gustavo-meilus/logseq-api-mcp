"""Tests for get_current_graph tool."""

from src.client.config import LogseqConfig
from tests.conftest import FakeLogseqClient
from src.tools.get_current_graph import get_current_graph as _run

_cfg = LogseqConfig("http://x", "t")

_GRAPH = {
    "name": "my-notes",
    "path": "/Users/me/Documents/my-notes",
    "url": "logseq://graph/my-notes",
}


class TestGetCurrentGraph:
    async def test_returns_graph_name(self):
        client = FakeLogseqClient({"get_current_graph": _GRAPH})
        result = await _run(client, _cfg)
        assert "my-notes" in result[0].text

    async def test_returns_graph_path(self):
        client = FakeLogseqClient({"get_current_graph": _GRAPH})
        result = await _run(client, _cfg)
        assert "/Users/me/Documents/my-notes" in result[0].text

    async def test_returns_no_graph_when_empty(self):
        client = FakeLogseqClient({"get_current_graph": {}})
        result = await _run(client, _cfg)
        assert "No active graph" in result[0].text

    async def test_returns_error_on_exception(self):
        class ErrorClient(FakeLogseqClient):
            async def get_current_graph(self):
                raise RuntimeError("not reachable")

        result = await _run(ErrorClient(), _cfg)
        assert "❌" in result[0].text
