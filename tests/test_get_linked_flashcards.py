"""Tests for get_linked_flashcards tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.get_linked_flashcards import get_linked_flashcards


class TestGetLinkedFlashcards:
    """Test cases for get_linked_flashcards function."""

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_success(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test successful linked flashcards retrieval."""
        sample_linked_refs = [
            [
                {"id": 789, "name": "Linked Page", "originalName": "Linked Page"},
                {
                    "id": 790,
                    "content": "What is the capital of France? #card",
                    "uuid": "ref-uuid-790",
                },
            ]
        ]

        sample_page_data = {"id": 123, "name": "test page", "originalName": "Test Page"}

        # Setup mock responses for all API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_linked_refs)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[sample_page_data])

        mock_blocks_response = MagicMock()
        mock_blocks_response.status = 200
        mock_blocks_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_context3 = MagicMock()
        mock_context3.__aenter__ = AsyncMock(return_value=mock_blocks_response)
        mock_context3.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
            mock_context3,
        ]

        result = await get_linked_flashcards("test page")

        assert len(result) == 1
        assert (
            "✅ No flashcards found in 'test page' or its linked pages"
            in result[0].text
        )

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_with_flashcards(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with actual flashcards."""
        sample_linked_refs = []

        sample_page_data = {"id": 123, "name": "test page", "originalName": "Test Page"}

        sample_blocks = [
            {
                "id": 456,
                "content": "What is the capital of France? #card",
                "uuid": "block-uuid-456",
                "properties": {"card-last-interval": 1},
                "children": [
                    ["uuid", "child-uuid-1"],
                ],
            }
        ]

        sample_child_block = {
            "id": 457,
            "content": "Paris is the capital of France",
            "uuid": "child-uuid-1",
        }

        # Setup mock responses for all API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_linked_refs)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[sample_page_data])

        mock_blocks_response = MagicMock()
        mock_blocks_response.status = 200
        mock_blocks_response.json = AsyncMock(return_value=sample_blocks)

        mock_child_response = MagicMock()
        mock_child_response.status = 200
        mock_child_response.json = AsyncMock(return_value=sample_child_block)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_context3 = MagicMock()
        mock_context3.__aenter__ = AsyncMock(return_value=mock_blocks_response)
        mock_context3.__aexit__ = AsyncMock(return_value=None)

        mock_context4 = MagicMock()
        mock_context4.__aenter__ = AsyncMock(return_value=mock_child_response)
        mock_context4.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
            mock_context3,
            mock_context4,
        ]

        result = await get_linked_flashcards("test page")

        assert len(result) == 1
        assert "🎯 **LINKED FLASHCARDS ANALYSIS**" in result[0].text
        assert "What is the capital of France?" in result[0].text
        assert "Paris is the capital of France" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_with_multiple_choice(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with multiple choice questions."""
        sample_linked_refs = []

        sample_page_data = {"id": 123, "name": "test page", "originalName": "Test Page"}

        sample_blocks = [
            {
                "id": 456,
                "content": "What is the capital of France? #card\n+ [ ] Paris\n+ [ ] London\n- [ ] Berlin",
                "uuid": "block-uuid-456",
                "properties": {},
                "children": [],
            }
        ]

        # Setup mock responses for all API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_linked_refs)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[sample_page_data])

        mock_blocks_response = MagicMock()
        mock_blocks_response.status = 200
        mock_blocks_response.json = AsyncMock(return_value=sample_blocks)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_context3 = MagicMock()
        mock_context3.__aenter__ = AsyncMock(return_value=mock_blocks_response)
        mock_context3.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
            mock_context3,
        ]

        result = await get_linked_flashcards("test page")

        assert len(result) == 1
        assert "🎯 **LINKED FLASHCARDS ANALYSIS**" in result[0].text
        assert "What is the capital of France?" in result[0].text
        assert "+ [ ] Paris" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_with_linked_pages(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with linked pages."""
        sample_linked_refs = [
            [
                {"id": 789, "name": "linked page", "originalName": "Linked Page"},
                {
                    "id": 790,
                    "content": "Reference content",
                    "uuid": "ref-uuid-790",
                },
            ]
        ]

        sample_page_data = [
            {"id": 123, "name": "test page", "originalName": "Test Page"},
            {"id": 789, "name": "linked page", "originalName": "Linked Page"},
        ]

        sample_blocks = []

        # Setup mock responses for all API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_linked_refs)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=sample_page_data)

        mock_blocks_response = MagicMock()
        mock_blocks_response.status = 200
        mock_blocks_response.json = AsyncMock(return_value=sample_blocks)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_context3 = MagicMock()
        mock_context3.__aenter__ = AsyncMock(return_value=mock_blocks_response)
        mock_context3.__aexit__ = AsyncMock(return_value=None)

        mock_context4 = MagicMock()
        mock_context4.__aenter__ = AsyncMock(return_value=mock_blocks_response)
        mock_context4.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
            mock_context3,
            mock_context4,
        ]

        result = await get_linked_flashcards("test page")

        assert len(result) == 1
        assert (
            "✅ No flashcards found in 'test page' or its linked pages"
            in result[0].text
        )

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_links_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with links HTTP error."""
        # Setup mock response for links call
        mock_links_response = MagicMock()
        mock_links_response.status = 500

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_linked_flashcards("Test Page")

        assert len(result) == 1
        assert "❌ Target page 'Test Page' not found" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_pages_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with pages HTTP error."""
        # Setup mock responses
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        mock_pages_response = MagicMock()
        mock_pages_response.status = 500

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_linked_flashcards("Test Page")

        assert len(result) == 1
        assert "❌ Target page 'Test Page' not found" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_blocks_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with blocks HTTP error."""
        sample_page_data = {"id": 123, "name": "test page", "originalName": "Test Page"}

        # Setup mock responses
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[sample_page_data])

        mock_blocks_response = MagicMock()
        mock_blocks_response.status = 500

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_context3 = MagicMock()
        mock_context3.__aenter__ = AsyncMock(return_value=mock_blocks_response)
        mock_context3.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
            mock_context3,
        ]

        result = await get_linked_flashcards("test page")

        assert len(result) == 1
        assert (
            "✅ No flashcards found in 'test page' or its linked pages"
            in result[0].text
        )

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_exception(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with exception."""
        # Setup session mock to raise exception
        mock_aiohttp_session._session_instance.post.side_effect = Exception(
            "Network error"
        )

        result = await get_linked_flashcards("Test Page")

        assert len(result) == 1
        assert "❌ Error fetching linked flashcards: Network error" in result[0].text
