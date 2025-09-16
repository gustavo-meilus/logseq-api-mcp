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
        sample_flashcard_data = {
            "content": "What is the capital of France? #card",
            "id": 789,
            "page": {"id": 123, "name": "Geography"},
            "properties": {"card-last-interval": 1, "card-repeats": 3},
        }

        sample_page_data = {"id": 123, "name": "Test Page", "originalName": "Test Page"}

        # Setup mock responses for both API calls
        mock_flashcards_response = MagicMock()
        mock_flashcards_response.status = 200
        mock_flashcards_response.json = AsyncMock(return_value=[sample_flashcard_data])

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[sample_page_data])

        # Setup session mock
        # Create separate mock contexts for each call
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_flashcards_response)
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
        assert "❌ Error fetching linked flashcards:" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_empty(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with empty result."""
        sample_page_data = {"id": 123, "name": "Test Page", "originalName": "Test Page"}

        # Setup mock responses for both API calls
        mock_flashcards_response = MagicMock()
        mock_flashcards_response.status = 200
        mock_flashcards_response.json = AsyncMock(return_value=[])

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[sample_page_data])

        # Setup session mock
        # Create separate mock contexts for each call
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_flashcards_response)
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
        assert "❌ Error fetching linked flashcards:" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_linked_flashcards("Test Page")

        assert len(result) == 1
        assert "❌ Target page 'Test Page' not found" in result[0].text

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
