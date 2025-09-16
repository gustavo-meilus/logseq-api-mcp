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

        # Setup mock responses for both API calls
        mock_flashcards_response = MagicMock()
        mock_flashcards_response.status = 200
        mock_flashcards_response.json = AsyncMock(return_value=[sample_flashcard_data])

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.side_effect = [
            mock_flashcards_response,
            mock_pages_response,
        ]
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_linked_flashcards("Test Page")

        assert len(result) == 1
        assert "💡 **LINKED FLASHCARDS**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_empty(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with empty result."""
        # Setup mock responses for both API calls
        mock_flashcards_response = MagicMock()
        mock_flashcards_response.status = 200
        mock_flashcards_response.json = AsyncMock(return_value=[])

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.side_effect = [
            mock_flashcards_response,
            mock_pages_response,
        ]
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_linked_flashcards("Test Page")

        assert len(result) == 1
        assert "✅ No flashcards found for 'Test Page'" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_linked_flashcards("Test Page")

        assert len(result) == 1
        assert "❌ Failed to fetch flashcards: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_get_linked_flashcards_exception(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test linked flashcards retrieval with exception."""
        # Setup session mock to raise exception
        mock_session_instance = AsyncMock()
        mock_session_instance.post.side_effect = Exception("Network error")
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_linked_flashcards("Test Page")

        assert len(result) == 1
        assert "❌ Error fetching linked flashcards: Network error" in result[0].text
