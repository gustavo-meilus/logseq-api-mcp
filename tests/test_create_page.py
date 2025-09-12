"""
Unit tests for create_page tool.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.types import TextContent

from tools.create_page import create_page


class TestCreatePage:
    """Test cases for create_page function."""

    @pytest.mark.asyncio
    async def test_create_page_success_basic(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful page creation with basic parameters."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await create_page("Test Page")

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        assert "📄 Page Name: Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_success_with_properties(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful page creation with properties."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        properties = {"status": "active", "priority": "high"}
        result = await create_page("Test Page", properties=properties)

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        assert "⚙️ Properties set: 2 items" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_success_with_format(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful page creation with format."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await create_page("Test Page", format="org")

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        assert "📝 Format: org" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_success_with_all_options(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test successful page creation with all options."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        properties = {"status": "active", "priority": "high"}
        result = await create_page(
            "Test Page", properties=properties, format="markdown"
        )

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        assert "⚙️ Properties set: 2 items" in result[0].text
        assert "📝 Format: markdown" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_success_with_detailed_response(
        self, mock_env_vars, mock_aiohttp_session, sample_page_data
    ):
        """Test successful page creation with detailed response data."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_page_data)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await create_page("Test Page")

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        assert "📊 **PAGE DETAILS:**" in result[0].text
        assert "• ID: 123" in result[0].text
        assert "• UUID: page-uuid-123" in result[0].text
        assert "• Original Name: Test Page" in result[0].text
        assert "• Format: markdown" in result[0].text
        assert "• Journal Page: No" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_success_with_properties_in_response(
        self, mock_env_vars, mock_aiohttp_session, sample_page_data
    ):
        """Test successful page creation with properties in response."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_page_data)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await create_page("Test Page")

        assert len(result) == 1
        assert "⚙️ **PAGE PROPERTIES:**" in result[0].text
        assert "• status: active" in result[0].text
        assert "• priority: high" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_success_journal_page(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test successful page creation for journal page."""
        journal_page_data = {
            "id": 123,
            "uuid": "journal-uuid-123",
            "name": "2024-01-15",
            "originalName": "2024-01-15",
            "journal?": True,
            "format": "markdown",
            "journalDay": 15,
        }

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=journal_page_data)
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await create_page("2024-01-15")

        assert len(result) == 1
        assert "• Journal Page: Yes" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test page creation with HTTP error."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        result = await create_page("Test Page")

        assert len(result) == 1
        assert "❌ Failed to create page: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_empty_response(
        self, mock_env_vars, mock_aiohttp_session, mock_empty_response
    ):
        """Test page creation with empty response."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_empty_response

        result = await create_page("Test Page")

        assert len(result) == 1
        assert "❌ Failed to create page: No response from Logseq API" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test page creation with exception."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.side_effect = (
            Exception("Network error")
        )

        result = await create_page("Test Page")

        assert len(result) == 1
        assert "❌ Error creating page: Network error" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_api_call_structure_basic(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that the API call is structured correctly for basic page creation."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        await create_page("Test Page")

        # Verify the API call was made with correct structure
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        mock_session.post.assert_called_once()

        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["method"] == "logseq.Editor.createPage"
        assert call_args[1]["json"]["args"] == ["Test Page"]

    @pytest.mark.asyncio
    async def test_create_page_api_call_structure_with_options(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that the API call is structured correctly with options."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        properties = {"status": "active"}
        await create_page("Test Page", properties=properties, format="org")

        # Verify the API call was made with correct structure
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        mock_session.post.assert_called_once()

        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["method"] == "logseq.Editor.createPage"
        expected_args = [
            "Test Page",
            {"properties": {"status": "active"}, "format": "org"},
        ]
        assert call_args[1]["json"]["args"] == expected_args

    @pytest.mark.asyncio
    async def test_create_page_headers(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that correct headers are sent."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        await create_page("Test Page")

        # Verify headers
        mock_session = mock_aiohttp_session.return_value.__aenter__.return_value
        call_args = mock_session.post.call_args
        assert call_args[1]["headers"]["Authorization"] == "Bearer test-token"

    @pytest.mark.asyncio
    async def test_create_page_next_steps(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test that next steps are included in the response."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await create_page("Test Page")

        assert "🔗 **NEXT STEPS:**" in result[0].text
        assert "• Check your Logseq graph to see the new page" in result[0].text
        assert "• Use get_all_pages to verify the page was created" in result[0].text
        assert "• Use append_block_in_page to add content to the page" in result[0].text
        assert "• Use get_page_blocks to view the page structure" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_empty_properties(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test page creation with empty properties dictionary."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await create_page("Test Page", properties={})

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        # Should not include properties info for empty dict
        assert "⚙️ Properties set:" not in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_none_properties(
        self, mock_env_vars, mock_aiohttp_session, mock_successful_response
    ):
        """Test page creation with None properties."""
        mock_aiohttp_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_successful_response

        result = await create_page("Test Page", properties=None)

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        # Should not include properties info for None
        assert "⚙️ Properties set:" not in result[0].text
