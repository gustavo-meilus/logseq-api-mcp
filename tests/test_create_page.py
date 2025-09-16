"""Tests for create_page tool."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools.create_page import create_page


class TestCreatePage:
    """Test cases for create_page function."""

    @pytest.mark.asyncio
    async def test_create_page_success_basic(self, mock_env_vars, mock_aiohttp_session):
        """Test successful page creation with basic parameters."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await create_page("Test Page")

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_with_properties(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test page creation with properties."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        properties = {"status": "active", "type": "note"}
        result = await create_page("Test Page", properties=properties)

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        assert "⚙️ **PAGE PROPERTIES:**" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_with_format(self, mock_env_vars, mock_aiohttp_session):
        """Test page creation with format."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await create_page("Test Page", format="markdown")

        assert len(result) == 1
        assert "✅ **PAGE CREATED SUCCESSFULLY**" in result[0].text
        assert "Format: markdown" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test page creation with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await create_page("Test Page")

        assert len(result) == 1
        assert "❌ Failed to create page: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_create_page_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test page creation with exception."""
        # Setup session mock to raise exception
        mock_session_instance = AsyncMock()
        mock_session_instance.post.side_effect = Exception("Network error")
        mock_aiohttp_session.return_value.__aenter__.return_value = (
            mock_session_instance
        )

        result = await create_page("Test Page")

        assert len(result) == 1
        assert "❌ Error creating page: Network error" in result[0].text
