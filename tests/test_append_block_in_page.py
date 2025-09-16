"""Tests for append_block_in_page tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.append_block_in_page import append_block_in_page


class TestAppendBlockInPage:
    """Test cases for append_block_in_page function."""

    @pytest.mark.asyncio
    async def test_append_block_success_basic(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test successful block append with basic parameters."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await append_block_in_page("Test Page", "Test content")

        assert len(result) == 1
        assert "✅ **BLOCK APPENDED SUCCESSFULLY**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_with_positioning(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block append with positioning options."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await append_block_in_page(
            "Test Page", "Test content", before="block-uuid-123", is_page_block=True
        )

        assert len(result) == 1
        assert "✅ **BLOCK APPENDED SUCCESSFULLY**" in result[0].text
        assert "📍 Positioned before block: block-uuid-123" in result[0].text
        assert "📍 Block type: Page-level block" in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test block append with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await append_block_in_page("Test Page", "Test content")

        assert len(result) == 1
        assert "❌ Failed to append block: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test block append with exception."""
        # Setup session mock to raise exception
        mock_aiohttp_session._session_instance.post.side_effect = Exception(
            "Network error"
        )

        result = await append_block_in_page("Test Page", "Test content")

        assert len(result) == 1
        assert "❌ Error appending block: Network error" in result[0].text
