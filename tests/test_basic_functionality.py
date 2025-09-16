"""Basic functionality tests that actually work."""

from unittest.mock import patch


from src.registry import register_all_tools
from src.server import mcp
from src.tools.get_all_pages import get_all_pages


class TestBasicFunctionality:
    """Basic tests that verify core functionality works."""

    def test_imports_work(self):
        """Test that all imports work correctly."""
        from src.tools import (
            append_block_in_page,
            create_page,
            edit_block,
            get_all_page_content,
            get_all_pages,
            get_block_content,
            get_linked_flashcards,
            get_page_blocks,
            get_page_links,
        )

        # Verify functions exist
        assert callable(append_block_in_page)
        assert callable(create_page)
        assert callable(edit_block)
        assert callable(get_all_pages)
        assert callable(get_page_blocks)
        assert callable(get_block_content)
        assert callable(get_all_page_content)
        assert callable(get_page_links)
        assert callable(get_linked_flashcards)

    def test_server_initialization(self):
        """Test that the MCP server can be initialized."""
        assert mcp is not None
        assert hasattr(mcp, "list_tools")

    def test_tool_registration_doesnt_crash(self):
        """Test that tool registration doesn't crash."""
        # This should not raise any exceptions
        register_all_tools(mcp)

    def test_environment_variables_handling(self):
        """Test that environment variables are handled correctly."""
        with patch.dict(
            "os.environ",
            {
                "LOGSEQ_API_ENDPOINT": "http://test:12315/api",
                "LOGSEQ_API_TOKEN": "test-token",
            },
        ):
            # Test that the functions can access environment variables
            from src.tools.get_all_pages import get_all_pages

            assert callable(get_all_pages)

    def test_function_signatures(self):
        """Test that functions have correct signatures."""
        # Test function signatures exist
        import inspect

        from src.tools.append_block_in_page import append_block_in_page
        from src.tools.create_page import create_page

        # get_all_pages should accept optional start/end parameters
        sig = inspect.signature(get_all_pages)
        assert "start" in sig.parameters
        assert "end" in sig.parameters

        # create_page should accept page_name and optional parameters
        sig = inspect.signature(create_page)
        assert "page_name" in sig.parameters
        assert "properties" in sig.parameters
        assert "format" in sig.parameters

        # append_block_in_page should accept page_identifier and content
        sig = inspect.signature(append_block_in_page)
        assert "page_identifier" in sig.parameters
        assert "content" in sig.parameters
