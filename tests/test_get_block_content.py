"""Tests for get_block_content tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.get_block_content import get_block_content


class TestGetBlockContent:
    """Test cases for get_block_content function."""

    @pytest.mark.asyncio
    async def test_get_block_content_success(
        self, mock_env_vars, mock_aiohttp_session, sample_block_data
    ):
        """Test successful block content retrieval."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "📋 **BLOCK CONTENT DETAILS**" in result[0].text
        assert "Test block content" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "❌ Failed to fetch block content: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_exception(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with exception."""
        # Setup session mock to raise exception
        mock_session_instance = AsyncMock()
        mock_session_instance.post.side_effect = Exception("Network error")
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "❌ Error fetching block content: Network error" in result[0].text
