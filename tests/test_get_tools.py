"""
Unit tests for all get_* tools.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.types import TextContent

from tools.get_all_page_content import get_all_page_content
from tools.get_all_pages import get_all_pages
from tools.get_block_content import get_block_content
from tools.get_linked_flashcards import get_linked_flashcards
from tools.get_page_blocks import get_page_blocks
from tools.get_page_links import get_page_links


class TestGetAllPages:
    """Test cases for get_all_pages function."""

    @pytest.mark.asyncio
    async def test_get_all_pages_success(self, mock_env_vars, mock_aiohttp_session):
        """Test successful pages retrieval."""
        sample_pages = [
            {
                "id": 1,
                "uuid": "page-uuid-1",
                "originalName": "Page 1",
                "name": "Page 1",
                "journal?": False,
                "createdAt": 1640995200000,
                "updatedAt": 1640995200000,
            },
            {
                "id": 2,
                "uuid": "page-uuid-2",
                "originalName": "2024-01-15",
                "name": "2024-01-15",
                "journal?": True,
                "createdAt": 1640995200000,
                "updatedAt": 1640995200000,
            },
        ]

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_pages)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_all_pages()

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "📊 **LOGSEQ PAGES LISTING**" in result[0].text
        assert "📈 Total pages: 2" in result[0].text
        assert "📅 Journal pages: 1" in result[0].text
        assert "📄 Regular pages: 1" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_pages_with_limits(self, mock_env_vars, mock_aiohttp_session):
        """Test pages retrieval with start/end limits."""
        sample_pages = [
            {
                "id": 1,
                "uuid": "page-uuid-1",
                "originalName": "Page 1",
                "name": "Page 1",
                "journal?": False,
                "createdAt": 1640995200000,
                "updatedAt": 1640995200000,
            },
            {
                "id": 2,
                "uuid": "page-uuid-2",
                "originalName": "Page 2",
                "name": "Page 2",
                "journal?": False,
                "createdAt": 1640995200000,
                "updatedAt": 1640995200000,
            },
            {
                "id": 3,
                "uuid": "page-uuid-3",
                "originalName": "Page 3",
                "name": "Page 3",
                "journal?": False,
                "createdAt": 1640995200000,
                "updatedAt": 1640995200000,
            },
        ]

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_pages)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_all_pages(start=0, end=2)

        assert len(result) == 1
        assert "showing indices 0-2" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_pages_empty(self, mock_env_vars, mock_aiohttp_session):
        """Test pages retrieval with empty result."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[])
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_all_pages()

        assert len(result) == 1
        assert "✅ No pages found in Logseq graph" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_pages_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test pages retrieval with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_all_pages()

        assert len(result) == 1
        assert "❌ Failed to fetch pages: HTTP 500" in result[0].text


class TestGetPageBlocks:
    """Test cases for get_page_blocks function."""

    @pytest.mark.asyncio
    async def test_get_page_blocks_success(
        self, mock_env_vars, mock_aiohttp_session, sample_block_data
    ):
        """Test successful page blocks retrieval."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[sample_block_data])
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_page_blocks("test-page")

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "🌳 **PAGE BLOCKS TREE STRUCTURE**" in result[0].text
        assert "📄 Page: Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_blocks_empty(self, mock_env_vars, mock_aiohttp_session):
        """Test page blocks retrieval with empty result."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[])
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_page_blocks("test-page")

        assert len(result) == 1
        assert "✅ Page 'test-page' has no blocks" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_blocks_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test page blocks retrieval with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_page_blocks("test-page")

        assert len(result) == 1
        assert "❌ Failed to fetch page blocks: HTTP 500" in result[0].text


class TestGetBlockContent:
    """Test cases for get_block_content function."""

    @pytest.mark.asyncio
    async def test_get_block_content_success(
        self, mock_env_vars, mock_aiohttp_session, sample_block_data
    ):
        """Test successful block content retrieval."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "📋 **BLOCK CONTENT DETAILS**" in result[0].text
        assert "🔗 UUID: block-uuid-456" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "❌ Failed to fetch block content: HTTP 500" in result[0].text


class TestGetAllPageContent:
    """Test cases for get_all_page_content function."""

    @pytest.mark.asyncio
    async def test_get_all_page_content_success(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test successful all page content retrieval."""
        sample_content = {
            "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
            "blocks": [
                {"id": 456, "content": "Test content", "uuid": "block-uuid-456"}
            ],
            "linkedPages": [
                {"id": 789, "name": "Linked Page", "uuid": "page-uuid-789"}
            ],
        }

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_content)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_all_page_content("test-page")

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "📄 **COMPREHENSIVE PAGE CONTENT**" in result[0].text
        assert "📄 Page: Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_all_page_content("test-page")

        assert len(result) == 1
        assert "❌ Failed to fetch page content: HTTP 500" in result[0].text


class TestGetPageLinks:
    """Test cases for get_page_links function."""

    @pytest.mark.asyncio
    async def test_get_page_links_success(self, mock_env_vars, mock_aiohttp_session):
        """Test successful page links retrieval."""
        sample_links = [
            {
                "id": 1,
                "uuid": "page-uuid-1",
                "originalName": "Linked Page 1",
                "name": "Linked Page 1",
                "journal?": False,
                "createdAt": 1640995200000,
                "updatedAt": 1640995200000,
            }
        ]

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_links)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_page_links("test-page")

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "🔗 **PAGE LINKS**" in result[0].text
        assert "📄 Target Page: test-page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_empty(self, mock_env_vars, mock_aiohttp_session):
        """Test page links retrieval with empty result."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[])
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_page_links("test-page")

        assert len(result) == 1
        assert "✅ No pages link to 'test-page'" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test page links retrieval with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_page_links("test-page")

        assert len(result) == 1
        assert "❌ Failed to fetch page links: HTTP 500" in result[0].text


class TestGetLinkedFlashcards:
    """Test cases for get_linked_flashcards function."""

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_success(
        self, mock_env_vars, mock_aiohttp_session, sample_flashcard_data
    ):
        """Test successful linked flashcards retrieval."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[sample_flashcard_data])
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_linked_flashcards("test-page")

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "💡 **LINKED FLASHCARDS**" in result[0].text
        assert "📄 Source Page: test-page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_empty(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with empty result."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[])
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_linked_flashcards("test-page")

        assert len(result) == 1
        assert "✅ No flashcards found for 'test-page'" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await get_linked_flashcards("test-page")

        assert len(result) == 1
        assert "❌ Failed to fetch flashcards: HTTP 500" in result[0].text


class TestCommonPatterns:
    """Test common patterns across all get tools."""

    @pytest.mark.asyncio
    async def test_all_tools_handle_exceptions(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test that all get tools handle exceptions properly."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.side_effect = (
            Exception("Network error")
        )

        # Test each tool
        tools_to_test = [
            (get_all_pages, []),
            (get_page_blocks, ["test-page"]),
            (get_block_content, ["block-uuid-123"]),
            (get_all_page_content, ["test-page"]),
            (get_page_links, ["test-page"]),
            (get_linked_flashcards, ["test-page"]),
        ]

        for tool_func, args in tools_to_test:
            result = await tool_func(*args)
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            assert "❌ Error" in result[0].text

    @pytest.mark.asyncio
    async def test_all_tools_use_correct_headers(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that all get tools use correct headers."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        # Test each tool
        tools_to_test = [
            (get_all_pages, []),
            (get_page_blocks, ["test-page"]),
            (get_block_content, ["block-uuid-123"]),
            (get_all_page_content, ["test-page"]),
            (get_page_links, ["test-page"]),
            (get_linked_flashcards, ["test-page"]),
        ]

        for tool_func, args in tools_to_test:
            await tool_func(*args)

            # Verify headers
            mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
            call_args = mock_session.post.call_args
            assert call_args[1]["headers"]["Authorization"] == "Bearer test-token"
