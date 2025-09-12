"""
Unit tests for append_block_in_page tool.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.types import TextContent

from tools.append_block_in_page import append_block_in_page


class TestAppendBlockInPage:
    """Test cases for append_block_in_page function."""

    @pytest.mark.asyncio
    async def test_append_block_success_basic(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block append with basic parameters."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await append_block_in_page("test-page", "Hello World")

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "✅ **BLOCK APPENDED SUCCESSFULLY**" in result[0].text
        assert "📄 Page: test-page" in result[0].text
        assert "📝 Content: Hello World" in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_success_with_options(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block append with all options."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await append_block_in_page(
            "test-page",
            "Hello World",
            before="block-uuid-123",
            sibling="block-uuid-456",
            is_page_block=True,
        )

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "✅ **BLOCK APPENDED SUCCESSFULLY**" in result[0].text
        assert "📍 Positioned before block: block-uuid-123" in result[0].text
        assert "📍 Positioned as sibling of: block-uuid-456" in result[0].text
        assert "📍 Block type: Page-level block" in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_success_with_before_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block append with before option only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await append_block_in_page(
            "test-page", "Hello World", before="block-uuid-123"
        )

        assert len(result) == 1
        assert "📍 Positioned before block: block-uuid-123" in result[0].text
        assert "📍 Positioned as sibling of:" not in result[0].text
        assert "📍 Block type:" not in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_success_with_sibling_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block append with sibling option only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await append_block_in_page(
            "test-page", "Hello World", sibling="block-uuid-456"
        )

        assert len(result) == 1
        assert "📍 Positioned as sibling of: block-uuid-456" in result[0].text
        assert "📍 Positioned before block:" not in result[0].text
        assert "📍 Block type:" not in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_success_with_page_block_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block append with is_page_block option only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await append_block_in_page(
            "test-page", "Hello World", is_page_block=True
        )

        assert len(result) == 1
        assert "📍 Block type: Page-level block" in result[0].text
        assert "📍 Positioned before block:" not in result[0].text
        assert "📍 Positioned as sibling of:" not in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_success_no_positioning(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block append with no positioning options."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await append_block_in_page("test-page", "Hello World")

        assert len(result) == 1
        assert "📍 Positioned: At the end of the page" in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test block append with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await append_block_in_page("test-page", "Hello World")

        assert len(result) == 1
        assert "❌ Failed to append block: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_empty_response(
        self, mock_env_vars, mock_aiohttp_session, mock_empty_response
    ):
        """Test block append with empty response."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_empty_response

        result = await append_block_in_page("test-page", "Hello World")

        assert len(result) == 1
        assert (
            "❌ Failed to append block: No response from Logseq API" in result[0].text
        )

    @pytest.mark.asyncio
    async def test_append_block_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test block append with exception."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.side_effect = (
            Exception("Network error")
        )

        result = await append_block_in_page("test-page", "Hello World")

        assert len(result) == 1
        assert "❌ Error appending block: Network error" in result[0].text

    @pytest.mark.asyncio
    async def test_append_block_api_call_structure(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that the API call is structured correctly."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        await append_block_in_page("test-page", "Hello World", before="block-123")

        # Verify the API call was made with correct structure
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        mock_session.post.assert_called_once()

        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["method"] == "logseq.Editor.appendBlockInPage"
        assert call_args[1]["json"]["args"] == [
            "test-page",
            "Hello World",
            {"before": "block-123"},
        ]

    @pytest.mark.asyncio
    async def test_append_block_api_call_no_options(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that the API call is structured correctly without options."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        await append_block_in_page("test-page", "Hello World")

        # Verify the API call was made with correct structure
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        mock_session.post.assert_called_once()

        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["method"] == "logseq.Editor.appendBlockInPage"
        assert call_args[1]["json"]["args"] == ["test-page", "Hello World"]

    @pytest.mark.asyncio
    async def test_append_block_headers(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that correct headers are sent."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        await append_block_in_page("test-page", "Hello World")

        # Verify headers
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        call_args = mock_session.post.call_args
        assert call_args[1]["headers"]["Authorization"] == "Bearer test-token"

    @pytest.mark.asyncio
    async def test_append_block_next_steps(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that next steps are included in the response."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await append_block_in_page("test-page", "Hello World")

        assert "🔗 **NEXT STEPS:**" in result[0].text
        assert "• Check your Logseq graph to see the new block" in result[0].text
        assert "• Use get_page_blocks to verify the block was added" in result[0].text
        assert (
            "• Use get_block_content to get details of the new block" in result[0].text
        )
