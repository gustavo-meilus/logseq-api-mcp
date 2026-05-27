"""WorkspaceConfigurator: pure, IO-free generator for Claude Code workspace config.

Given a Logseq graph info dict and LogseqConfig, produces:
- A .mcp.json content string pre-filled with the active token and URL
- The target file path inside the graph folder
- A one-liner claude mcp add-json install command

No network, no filesystem access. Fully unit-testable.
"""

import json

from src.client.config import LogseqConfig

_GITHUB_URL = "git+https://github.com/gustavo-meilus/logseq-api-mcp"


class WorkspaceConfigurator:
    """Generate Claude Code workspace config for a Logseq graph.

    Args:
        graph_info: Dict from logseq.App.getCurrentGraph with 'name', 'path', 'url'.
        config: Active LogseqConfig (provides token and endpoint URL).

    Complexity: O(1) construction; O(1) per method.
    """

    def __init__(self, graph_info: dict, config: LogseqConfig) -> None:
        self._graph_info = graph_info
        self._config = config

    def _api_url(self) -> str:
        """Derive the base URL from the endpoint (strip /api suffix)."""
        endpoint = self._config.endpoint
        if endpoint.endswith("/api"):
            return endpoint[: -len("/api")]
        return endpoint

    def mcp_json_content(self) -> str:
        """Return a formatted .mcp.json string pre-filled with active credentials.

        Returns:
            JSON string with mcpServers.logseq entry using uvx + GitHub URL.
        """
        config = {
            "mcpServers": {
                "logseq": {
                    "command": "uvx",
                    "args": [_GITHUB_URL],
                    "env": {
                        "LOGSEQ_API_TOKEN": self._config.token,
                        "LOGSEQ_API_URL": self._api_url(),
                    },
                }
            }
        }
        return json.dumps(config, indent=2)

    def target_path(self) -> str:
        """Return the absolute path where .mcp.json should be written.

        Returns:
            '{graph_path}/.mcp.json'
        """
        graph_path = self._graph_info.get("path", "")
        return f"{graph_path}/.mcp.json"

    def install_command(self) -> str:
        """Return a one-liner claude mcp add-json command with active credentials.

        Returns:
            Shell command string the user can run to register the MCP server.
        """
        env_json = json.dumps(
            {
                "command": "uvx",
                "args": [_GITHUB_URL],
                "env": {
                    "LOGSEQ_API_TOKEN": self._config.token,
                    "LOGSEQ_API_URL": self._api_url(),
                },
            }
        )
        return f"claude mcp add-json logseq '{env_json}'"
