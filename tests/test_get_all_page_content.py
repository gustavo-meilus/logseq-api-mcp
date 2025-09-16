"""Tests for get_all_page_content tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.get_all_page_content import get_all_page_content


class TestGetAllPageContent:
    """Test cases for get_all_page_content function."""

    @pytest.mark.asyncio
    async def test_get_all_page_content_success(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test successful all page content retrieval."""
        sample_content = [
            {
                "id": 456,
                "content": "Test content",
                "uuid": "block-uuid-456",
                "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
            }
        ]

        # Setup mock responses for both API calls
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        # Setup session mock
        # Create separate mock contexts for each call
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_content_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "📄 **COMPREHENSIVE CONTENT:**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_with_flashcards(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with flashcard content."""
        sample_content = [
            {
                "id": 456,
                "content": "What is the capital of France? #card",
                "uuid": "block-uuid-456",
                "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
                "properties": {"card-last-interval": 1},
            }
        ]

        # Setup mock responses for both API calls
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_content_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "📄 **Flashcard**" in result[0].text
        assert "What is the capital of France?" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_with_children(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with child blocks."""
        sample_content = [
            {
                "id": 456,
                "content": "Parent block",
                "uuid": "block-uuid-456",
                "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
                "children": [
                    {
                        "id": 457,
                        "content": "Child block 1",
                        "uuid": "block-uuid-457",
                    },
                    {
                        "id": 458,
                        "content": "Child block 2",
                        "uuid": "block-uuid-458",
                    },
                ],
            }
        ]

        # Setup mock responses for both API calls
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_content_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "Parent block" in result[0].text
        assert "Child block 1" in result[0].text
        assert "Child block 2" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_with_linked_references(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with linked references."""
        sample_content = [
            {
                "id": 456,
                "content": "Test content",
                "uuid": "block-uuid-456",
                "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
            }
        ]

        sample_links = [
            [
                {"id": 789, "name": "Linked Page", "originalName": "Linked Page"},
                {
                    "id": 790,
                    "content": "Reference content #card",
                    "uuid": "ref-uuid-790",
                },
            ]
        ]

        # Setup mock responses for both API calls
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_links)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_content_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "🔗 **LINKED REFERENCES:**" in result[0].text
        assert "Linked Page" in result[0].text
        assert "Reference content" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_empty_blocks(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with empty blocks."""
        sample_content = []

        # Setup mock responses for both API calls
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_content_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "✅ Page: Test Page - No content found" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_with_properties(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with block properties."""
        sample_content = [
            {
                "id": 456,
                "content": "Test content",
                "uuid": "block-uuid-456",
                "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
                "properties": {
                    "important": "yes",
                    "tags": ["test", "example"],
                    "collapsed": True,  # Should be filtered out
                },
            }
        ]

        # Setup mock responses for both API calls
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_content_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "important: yes" in result[0].text
        assert "tags: test, example" in result[0].text
        assert "collapsed" not in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_with_code_blocks(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with code blocks."""
        sample_content = [
            {
                "id": 456,
                "content": "```python\nprint('Hello World')\n```",
                "uuid": "block-uuid-456",
                "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
            }
        ]

        # Setup mock responses for both API calls
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_content_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "📄 **```python**" in result[0].text
        assert "```python" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_links_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with links HTTP error."""
        sample_content = [
            {
                "id": 456,
                "content": "Test content",
                "uuid": "block-uuid-456",
                "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
            }
        ]

        # Setup mock responses - content succeeds, links fail
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 500

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_content_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "📄 **COMPREHENSIVE CONTENT:**" in result[0].text
        assert "🔗 **LINKED REFERENCES:**" in result[0].text
        assert "No linked references found" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "❌ Failed to fetch page blocks: 500" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_exception(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with exception."""
        # Setup session mock to raise exception
        mock_aiohttp_session._session_instance.post.side_effect = Exception(
            "Network error"
        )

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "❌ Error getting page content: Network error" in result[0].text
