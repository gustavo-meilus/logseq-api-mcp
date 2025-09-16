"""Tests for get_all_pages tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.get_all_pages import get_all_pages


class TestGetAllPages:
    """Test cases for get_all_pages function."""

    @pytest.mark.asyncio
    async def test_get_all_pages_success(
        self, mock_env_vars, mock_aiohttp_session, sample_page_data
    ):
        """Test successful pages retrieval."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[sample_page_data])

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await get_all_pages()

        assert len(result) == 1
        assert "📊 **LOGSEQ PAGES LISTING**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_pages_with_limits(
        self, mock_env_vars, mock_aiohttp_session, sample_page_data
    ):
        """Test pages retrieval with start/end limits."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[sample_page_data])

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await get_all_pages(start=0, end=1)

        assert len(result) == 1
        assert "showing indices 0-1" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_pages_empty(self, mock_env_vars, mock_aiohttp_session):
        """Test pages retrieval with empty result."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await get_all_pages()

        assert len(result) == 1
        assert "✅ No pages found in Logseq graph" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_pages_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test pages retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await get_all_pages()

        assert len(result) == 1
        assert "❌ Failed to fetch pages: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_get_all_pages_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test pages retrieval with exception."""
        # Setup session mock to raise exception
        mock_aiohttp_session._session_instance.post.side_effect = Exception(
            "Network error"
        )

        result = await get_all_pages()

        assert len(result) == 1
        assert "❌ Error fetching pages: Network error" in result[0].text
