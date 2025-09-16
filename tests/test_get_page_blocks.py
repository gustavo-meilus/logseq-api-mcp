"""Tests for get_page_blocks tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.get_page_blocks import get_page_blocks


class TestGetPageBlocks:
    """Test cases for get_page_blocks function."""

    @pytest.mark.asyncio
    async def test_get_page_blocks_success(
        self, mock_env_vars, mock_aiohttp_session, sample_block_data
    ):
        """Test successful page blocks retrieval."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[sample_block_data])

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_page_blocks("Test Page")

        assert len(result) == 1
        assert "🌳 **PAGE BLOCKS TREE STRUCTURE**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_blocks_empty(self, mock_env_vars, mock_aiohttp_session):
        """Test page blocks retrieval with empty result."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[])

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_page_blocks("Test Page")

        assert len(result) == 1
        assert "✅ Page 'Test Page' has no blocks" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_blocks_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test page blocks retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_page_blocks("Test Page")

        assert len(result) == 1
        assert "❌ Failed to fetch page blocks: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_blocks_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test page blocks retrieval with exception."""
        # Setup session mock to raise exception
        mock_session_instance = AsyncMock()
        mock_session_instance.post.side_effect = Exception("Network error")
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_page_blocks("Test Page")

        assert len(result) == 1
        assert "❌ Error fetching page blocks: Network error" in result[0].text
