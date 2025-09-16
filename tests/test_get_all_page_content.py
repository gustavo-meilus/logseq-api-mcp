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
        sample_content = {
            "page": {"id": 123, "name": "Test Page", "uuid": "page-uuid-123"},
            "blocks": [
                {"id": 456, "content": "Test content", "uuid": "block-uuid-456"}
            ],
            "linkedPages": [
                {"id": 789, "name": "Linked Page", "uuid": "page-uuid-789"}
            ],
        }

        # Setup mock responses for both API calls
        mock_content_response = MagicMock()
        mock_content_response.status = 200
        mock_content_response.json = AsyncMock(return_value=sample_content)

        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.side_effect = [
            mock_content_response,
            mock_links_response,
        ]
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "📄 **COMPREHENSIVE PAGE CONTENT**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "❌ Failed to fetch page content: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_page_content_exception(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test all page content retrieval with exception."""
        # Setup session mock to raise exception
        mock_session_instance = AsyncMock()
        mock_session_instance.post.side_effect = Exception("Network error")
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_all_page_content("Test Page")

        assert len(result) == 1
        assert "❌ Error getting page content: Network error" in result[0].text
