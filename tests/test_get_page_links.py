"""Tests for get_page_links tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.get_page_links import get_page_links


class TestGetPageLinks:
    """Test cases for get_page_links function."""

    @pytest.mark.asyncio
    async def test_get_page_links_success(
        self, mock_env_vars, mock_aiohttp_session, sample_page_data
    ):
        """Test successful page links retrieval."""
        # Setup mock responses for both API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[sample_page_data])

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[sample_page_data])

        # Setup session mock
        mock_session_instance = AsyncMock()
        # Mock both post calls
        mock_session_instance.post.return_value.__aenter__.side_effect = [
            mock_links_response,
            mock_pages_response,
        ]
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "🔗 **PAGE LINKS**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_empty(self, mock_env_vars, mock_aiohttp_session):
        """Test page links retrieval with empty result."""
        # Setup mock responses for both API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=[])

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.side_effect = [
            mock_links_response,
            mock_pages_response,
        ]
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "✅ No pages link to 'Test Page'" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test page links retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "❌ Failed to fetch page links: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test page links retrieval with exception."""
        # Setup session mock to raise exception
        mock_session_instance = AsyncMock()
        mock_session_instance.post.side_effect = Exception("Network error")
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "❌ Error fetching page links: Network error" in result[0].text
