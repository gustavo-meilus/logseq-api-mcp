"""FastMCP entry point for logseq-api-mcp."""

import os

from mcp.server.fastmcp import FastMCP

from .client.config import load_config
from .client.logseq_client import LogseqClient
from .logging_setup import setup_logging
from .registry import register_all_tools


setup_logging()

mcp = FastMCP("Logseq API")

_config = load_config() if os.getenv("LOGSEQ_API_TOKEN") else None
if _config is not None:
    _client = LogseqClient(_config)
    register_all_tools(mcp, _client, _config)


def main() -> None:
    """Console script entry point for uvx / pip install."""
    mcp.run()


if __name__ == "__main__":
    main()
