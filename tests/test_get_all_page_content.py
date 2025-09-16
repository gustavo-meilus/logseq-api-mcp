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
