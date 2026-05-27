"""Tests for suggest_workspace tool and WorkspaceConfigurator."""

import json

from src.client.config import LogseqConfig
from src.workspace.configurator import WorkspaceConfigurator
from tests.conftest import FakeLogseqClient
from src.tools.suggest_workspace import suggest_workspace as _run

_cfg = LogseqConfig(
    endpoint="http://127.0.0.1:12315/api",
    token="my-secret-token",
)

_GRAPH = {
    "name": "my-notes",
    "path": "/Users/me/Documents/my-notes",
    "url": "logseq://graph/my-notes",
}


# ── WorkspaceConfigurator (pure unit tests, no mocks) ────────────────────────


class TestWorkspaceConfigurator:
    def test_mcp_json_content_is_valid_json(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        content = wc.mcp_json_content()
        parsed = json.loads(content)
        assert "mcpServers" in parsed

    def test_mcp_json_contains_logseq_server_key(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        parsed = json.loads(wc.mcp_json_content())
        assert "logseq" in parsed["mcpServers"]

    def test_mcp_json_uses_uvx_command(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        parsed = json.loads(wc.mcp_json_content())
        server = parsed["mcpServers"]["logseq"]
        assert server["command"] == "uvx"

    def test_mcp_json_contains_github_url_arg(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        parsed = json.loads(wc.mcp_json_content())
        args = parsed["mcpServers"]["logseq"]["args"]
        assert any("github.com/gustavo-meilus/logseq-api-mcp" in a for a in args)

    def test_mcp_json_token_comes_from_config(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        parsed = json.loads(wc.mcp_json_content())
        env = parsed["mcpServers"]["logseq"]["env"]
        assert env["LOGSEQ_API_TOKEN"] == "my-secret-token"

    def test_mcp_json_url_comes_from_config_endpoint(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        parsed = json.loads(wc.mcp_json_content())
        env = parsed["mcpServers"]["logseq"]["env"]
        assert "LOGSEQ_API_URL" in env

    def test_target_path_appends_mcp_json_to_graph_path(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        assert wc.target_path() == "/Users/me/Documents/my-notes/.mcp.json"

    def test_install_command_contains_claude_mcp_add_json(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        cmd = wc.install_command()
        assert "claude mcp add-json" in cmd

    def test_install_command_contains_token(self):
        wc = WorkspaceConfigurator(graph_info=_GRAPH, config=_cfg)
        cmd = wc.install_command()
        assert "my-secret-token" in cmd


# ── suggest_workspace tool ───────────────────────────────────────────────────


class TestSuggestWorkspace:
    async def test_returns_graph_path_in_output(self):
        client = FakeLogseqClient({"get_current_graph": _GRAPH})
        result = await _run(client, _cfg)
        assert "/Users/me/Documents/my-notes" in result[0].text

    async def test_returns_mcp_json_content_in_output(self):
        client = FakeLogseqClient({"get_current_graph": _GRAPH})
        result = await _run(client, _cfg)
        assert "mcpServers" in result[0].text

    async def test_returns_target_path_in_output(self):
        client = FakeLogseqClient({"get_current_graph": _GRAPH})
        result = await _run(client, _cfg)
        assert ".mcp.json" in result[0].text

    async def test_returns_install_command_in_output(self):
        client = FakeLogseqClient({"get_current_graph": _GRAPH})
        result = await _run(client, _cfg)
        assert "claude mcp add-json" in result[0].text

    async def test_returns_no_graph_message_when_graph_empty(self):
        client = FakeLogseqClient({"get_current_graph": {}})
        result = await _run(client, _cfg)
        assert "No active graph" in result[0].text

    async def test_returns_error_on_exception(self):
        class ErrorClient(FakeLogseqClient):
            async def get_current_graph(self):
                raise RuntimeError("unreachable")

        result = await _run(ErrorClient(), _cfg)
        assert "❌" in result[0].text
