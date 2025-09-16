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
        # Mock both post calls
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "🔗 **PAGE LINKS ANALYSIS**" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_with_multiple_references(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test page links retrieval with multiple references."""
        sample_links = [
            [
                {"id": 123, "name": "Page 1", "originalName": "Page 1"},
                {"id": 456, "content": "Reference 1", "uuid": "ref-1"},
                {"id": 457, "content": "Reference 2", "uuid": "ref-2"},
            ],
            [
                {"id": 789, "name": "Page 2", "originalName": "Page 2"},
                {"id": 101, "content": "Reference 3", "uuid": "ref-3"},
            ],
        ]

        sample_pages = [
            {
                "id": 123,
                "name": "Page 1",
                "originalName": "Page 1",
                "createdAt": 1640995200000,  # 2022-01-01
                "updatedAt": 1640995200000,
                "journal?": False,
                "uuid": "page-uuid-1",
                "properties": {"important": "yes"},
            },
            {
                "id": 789,
                "name": "Page 2",
                "originalName": "Page 2",
                "createdAt": 1640995200000,
                "updatedAt": 1640995200000,
                "journal?": True,
                "uuid": "page-uuid-2",
                "properties": {"tags": ["test"]},
            },
        ]

        # Setup mock responses for both API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_links)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=sample_pages)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "🔗 **PAGE LINKS ANALYSIS**" in result[0].text
        assert "Page 1" in result[0].text
        assert "Page 2" in result[0].text
        assert "📅" in result[0].text  # Journal page emoji
        assert "📄" in result[0].text  # Regular page emoji

    @pytest.mark.asyncio
    async def test_get_page_links_with_properties(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test page links retrieval with page properties."""
        sample_links = [
            [
                {"id": 123, "name": "Page 1", "originalName": "Page 1"},
                {"id": 456, "content": "Reference 1", "uuid": "ref-1"},
            ]
        ]

        sample_pages = [
            {
                "id": 123,
                "name": "Page 1",
                "originalName": "Page 1",
                "createdAt": 1640995200000,
                "updatedAt": 1640995200000,
                "journal?": False,
                "uuid": "page-uuid-1",
                "properties": {
                    "important": "yes",
                    "tags": ["test", "example"],
                    "priority": 1,
                    "collapsed": True,  # Should be filtered out
                },
            }
        ]

        # Setup mock responses for both API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_links)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=sample_pages)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "🔗 **PAGE LINKS ANALYSIS**" in result[0].text
        assert "important: yes" in result[0].text
        assert "tags: test, example" in result[0].text
        assert "priority: 1" in result[0].text
        assert "collapsed" not in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_with_timestamps(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test page links retrieval with timestamp formatting."""
        sample_links = [
            [
                {"id": 123, "name": "Page 1", "originalName": "Page 1"},
                {"id": 456, "content": "Reference 1", "uuid": "ref-1"},
            ]
        ]

        sample_pages = [
            {
                "id": 123,
                "name": "Page 1",
                "originalName": "Page 1",
                "createdAt": 1640995200000,  # 2022-01-01 00:00:00
                "updatedAt": 1640995200000,
                "journal?": False,
                "uuid": "page-uuid-1",
                "properties": {},
            }
        ]

        # Setup mock responses for both API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_links)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=sample_pages)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "🔗 **PAGE LINKS ANALYSIS**" in result[0].text
        assert "Page 1" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_with_invalid_timestamps(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test page links retrieval with invalid timestamps."""
        sample_links = [
            [
                {"id": 123, "name": "Page 1", "originalName": "Page 1"},
                {"id": 456, "content": "Reference 1", "uuid": "ref-1"},
            ]
        ]

        sample_pages = [
            {
                "id": 123,
                "name": "Page 1",
                "originalName": "Page 1",
                "createdAt": "invalid-timestamp",
                "updatedAt": None,
                "journal?": False,
                "uuid": "page-uuid-1",
                "properties": {},
            }
        ]

        # Setup mock responses for both API calls
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_links)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 200
        mock_pages_response.json = AsyncMock(return_value=sample_pages)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "🔗 **PAGE LINKS ANALYSIS**" in result[0].text
        assert "invalid-timestamp" in result[0].text
        assert "N/A" in result[0].text

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
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "✅ No pages link to 'Test Page'" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_pages_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test page links retrieval with pages HTTP error."""
        sample_links = [
            [
                {"id": 123, "name": "Page 1", "originalName": "Page 1"},
                {"id": 456, "content": "Reference 1", "uuid": "ref-1"},
            ]
        ]

        # Setup mock responses
        mock_links_response = MagicMock()
        mock_links_response.status = 200
        mock_links_response.json = AsyncMock(return_value=sample_links)

        mock_pages_response = MagicMock()
        mock_pages_response.status = 500

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_links_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_pages_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "🔗 **PAGE LINKS ANALYSIS**" in result[0].text
        assert "Page 1" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_http_error(self, mock_env_vars, mock_aiohttp_session):
        """Test page links retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "❌ Failed to fetch page links: HTTP 500" in result[0].text

    @pytest.mark.asyncio
    async def test_get_page_links_exception(self, mock_env_vars, mock_aiohttp_session):
        """Test page links retrieval with exception."""
        # Setup session mock to raise exception
        mock_aiohttp_session._session_instance.post.side_effect = Exception(
            "Network error"
        )

        result = await get_page_links("Test Page")

        assert len(result) == 1
        assert "❌ Error fetching page links: Network error" in result[0].text
