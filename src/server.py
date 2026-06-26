"""FastMCP entry point for logseq-api-mcp."""

import os

from mcp.server.fastmcp import FastMCP

try:
    from .client.config import load_config
    from .client.logseq_client import LogseqClient
    from .logging_setup import setup_logging
    from .registry import register_all_tools
except ImportError:
    # mcp dev loads files via importlib without package context (__package__ = None).
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from src.client.config import load_config  # type: ignore[no-redef]
    from src.client.logseq_client import LogseqClient  # type: ignore[no-redef]
    from src.logging_setup import setup_logging  # type: ignore[no-redef]
    from src.registry import register_all_tools  # type: ignore[no-redef]


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
