"""
Unit tests for edit_block tool.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.types import TextContent

from tools.edit_block import edit_block


class TestEditBlock:
    """Test cases for edit_block function."""

    @pytest.mark.asyncio
    async def test_edit_block_success_content_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with content only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await edit_block("block-uuid-123", content="Updated content")

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "🔗 Block UUID: block-uuid-123" in result[0].text
        assert "📝 Content updated" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_properties_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with properties only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        properties = {"status": "completed", "priority": "high"}
        result = await edit_block("block-uuid-123", properties=properties)

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "⚙️ Properties updated (2 items)" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_cursor_position_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with cursor position only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await edit_block("block-uuid-123", cursor_position=10)

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "📍 Cursor positioned at index 10" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_focus_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with focus only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await edit_block("block-uuid-123", focus=True)

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "🎯 Focus: Enabled" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_focus_disabled(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with focus disabled."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await edit_block("block-uuid-123", focus=False)

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "🎯 Focus: Disabled" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_all_options(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with all options."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        properties = {"status": "completed", "priority": "high"}
        result = await edit_block(
            "block-uuid-123",
            content="Updated content",
            properties=properties,
            cursor_position=15,
            focus=True,
        )

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "📝 Content updated" in result[0].text
        assert "⚙️ Properties updated (2 items)" in result[0].text
        assert "📍 Cursor positioned at index 15" in result[0].text
        assert "🎯 Focus: Enabled" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_with_content_preview(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with content preview."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        long_content = "This is a very long content that should be truncated in the preview because it exceeds the 100 character limit for display purposes"
        result = await edit_block("block-uuid-123", content=long_content)

        assert len(result) == 1
        assert "📝 **UPDATED CONTENT:**" in result[0].text
        assert "```" in result[0].text
        assert (
            "This is a very long content that should be truncated in the preview because it exceeds the 100 character limit..."
            in result[0].text
        )

    @pytest.mark.asyncio
    async def test_edit_block_success_with_short_content(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with short content (no truncation)."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        short_content = "Short content"
        result = await edit_block("block-uuid-123", content=short_content)

        assert len(result) == 1
        assert "📝 **UPDATED CONTENT:**" in result[0].text
        assert "```" in result[0].text
        assert "Short content" in result[0].text
        assert "..." not in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_with_properties_display(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful block edit with properties display."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        properties = {"status": "completed", "priority": "high", "type": "note"}
        result = await edit_block("block-uuid-123", properties=properties)

        assert len(result) == 1
        assert "⚙️ **UPDATED PROPERTIES:**" in result[0].text
        assert "• status: completed" in result[0].text
        assert "• priority: high" in result[0].text
        assert "• type: note" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_success_with_detailed_response(
        self, mock_env_vars, mock_aiohttp_session, sample_block_data
    ):
        """Test successful block edit with detailed response data."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await edit_block("block-uuid-123", content="Updated content")

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "📋 **BLOCK INFORMATION:**" in result[0].text
        assert "• ID: 456" in result[0].text
        assert "• UUID: block-uuid-456" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test block edit with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await edit_block("block-uuid-123", content="Updated content")

        assert len(result) == 1
        assert "❌ Failed to edit block: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_empty_response(
        self, mock_env_vars, mock_aiohttp_session, mock_empty_response
    ):
        """Test block edit with empty response."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_empty_response

        result = await edit_block("block-uuid-123", content="Updated content")

        assert len(result) == 1
        assert "❌ Failed to edit block: No response from Logseq API" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test block edit with exception."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.side_effect = (
            Exception("Network error")
        )

        result = await edit_block("block-uuid-123", content="Updated content")

        assert len(result) == 1
        assert "❌ Error editing block: Network error" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_api_call_structure_content_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that the API call is structured correctly for content only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        await edit_block("block-uuid-123", content="Updated content")

        # Verify the API call was made with correct structure
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        mock_session.post.assert_called_once()

        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["method"] == "logseq.Editor.editBlock"
        assert call_args[1]["json"]["args"] == ["block-uuid-123", "Updated content"]

    @pytest.mark.asyncio
    async def test_edit_block_api_call_structure_with_all_options(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that the API call is structured correctly with all options."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        properties = {"status": "completed"}
        await edit_block(
            "block-uuid-123",
            content="Updated content",
            properties=properties,
            cursor_position=10,
            focus=True,
        )

        # Verify the API call was made with correct structure
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        mock_session.post.assert_called_once()

        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["method"] == "logseq.Editor.editBlock"
        expected_args = [
            "block-uuid-123",
            "Updated content",
            {"status": "completed"},
            {"pos": 10, "focus": True},
        ]
        assert call_args[1]["json"]["args"] == expected_args

    @pytest.mark.asyncio
    async def test_edit_block_api_call_structure_properties_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that the API call is structured correctly for properties only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        properties = {"status": "completed"}
        await edit_block("block-uuid-123", properties=properties)

        # Verify the API call was made with correct structure
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        mock_session.post.assert_called_once()

        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["method"] == "logseq.Editor.editBlock"
        expected_args = ["block-uuid-123", {"status": "completed"}]
        assert call_args[1]["json"]["args"] == expected_args

    @pytest.mark.asyncio
    async def test_edit_block_api_call_structure_options_only(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that the API call is structured correctly for options only."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        await edit_block("block-uuid-123", cursor_position=5, focus=True)

        # Verify the API call was made with correct structure
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        mock_session.post.assert_called_once()

        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["method"] == "logseq.Editor.editBlock"
        expected_args = ["block-uuid-123", {"pos": 5, "focus": True}]
        assert call_args[1]["json"]["args"] == expected_args

    @pytest.mark.asyncio
    async def test_edit_block_headers(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that correct headers are sent."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        await edit_block("block-uuid-123", content="Updated content")

        # Verify headers
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        call_args = mock_session.post.call_args
        assert call_args[1]["headers"]["Authorization"] == "Bearer test-token"

    @pytest.mark.asyncio
    async def test_edit_block_next_steps(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that next steps are included in the response."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await edit_block("block-uuid-123", content="Updated content")

        assert "🔗 **NEXT STEPS:**" in result[0].text
        assert "• Check your Logseq graph to see the updated block" in result[0].text
        assert "• Use get_block_content to verify the changes" in result[0].text
        assert "• Use get_page_blocks to see the block in context" in result[0].text

    @pytest.mark.asyncio
    async def test_edit_block_no_edit_details_when_nothing_provided(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that no edit details are shown when no edit parameters are provided."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await edit_block("block-uuid-123")

        assert len(result) == 1
        assert "✅ **BLOCK EDITED SUCCESSFULLY**" in result[0].text
        assert "📊 **EDIT DETAILS:**" not in result[0].text
        assert "📝 Content updated" not in result[0].text
        assert "⚙️ Properties updated" not in result[0].text
        assert "📍 Cursor positioned" not in result[0].text
        assert "🎯 Focus:" not in result[0].text
