"""Tests for edit_block tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.edit_block import edit_block


class TestEditBlock:
    """Test cases for edit_block function."""

    @pytest.mark.asyncio
    async def test_edit_block_success_content(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test successful block edit with content."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await edit_block("block-uuid-123", content="Updated content")

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "📝 **UPDATED CONTENT:**" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_properties(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test successful block edit with properties."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        properties = {"status": "completed", "priority": "high"}
        result = await edit_block("block-uuid-123", properties=properties)

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "⚙️ **UPDATED PROPERTIES:**" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_options(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test successful block edit with options."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await edit_block(
            "block-uuid-123", content="Updated content", cursor_position=10, focus=True
        )

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test block edit with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_aiohttp_session._post_context.__aenter__ = AsyncMock(
            return_value=mock_response
        )
        mock_aiohttp_session._post_context.__aexit__ = AsyncMock(return_value=None)

        result = await edit_block("block-uuid-123", content="Updated content")

        assert len(result) == 1
        assert "❌ Failed to edit block: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test block edit with exception."""
        # Setup session mock to raise exception
        mock_aiohttp_session._session_instance.post.side_effect = Exception(
            "Network error"
        )

        result = await edit_block("block-uuid-123", content="Updated content")

        assert len(result) == 1
        assert "❌ Error editing block: Network error" in result[0].text
