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
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert "Test block content" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_with_children(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with child blocks."""
        sample_block_data = {
            "id": 456,
            "content": "Parent block content",
            "uuid": "block-uuid-456",
            "properties": {"important": "yes"},
            "children": [
                ["uuid", "child-uuid-1"],
                ["uuid", "child-uuid-2"],
            ],
            "parent": {"id": 123},
            "page": {"id": 789, "name": "Test Page"},
        }

        sample_child_data = {
            "id": 457,
            "content": "Child block content",
            "uuid": "child-uuid-1",
            "properties": {},
            "children": [],
        }

        # Setup mock responses
        mock_main_response = MagicMock()
        mock_main_response.status = 200
        mock_main_response.json = AsyncMock(return_value=sample_block_data)

        mock_child_response = MagicMock()
        mock_child_response.status = 200
        mock_child_response.json = AsyncMock(return_value=sample_child_data)

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_main_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_child_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
            mock_context2,  # Second child
        ]

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert "Parent block content" in result[0].text
        assert "👶 **CHILD BLOCK**" in result[0].text
        assert "Child block content" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_with_flashcard(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with flashcard content."""
        sample_block_data = {
            "id": 456,
            "content": "What is the capital of France? #card",
            "uuid": "block-uuid-456",
            "properties": {"card-last-interval": 1},
            "children": [],
            "parent": {"id": 123},
            "page": {"id": 789, "name": "Test Page"},
        }

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert "💡 Flashcard" in result[0].text
        assert "What is the capital of France?" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_with_code_block(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with code block content."""
        sample_block_data = {
            "id": 456,
            "content": "```python\nprint('Hello World')\n```",
            "uuid": "block-uuid-456",
            "properties": {},
            "children": [],
            "parent": {"id": 123},
            "page": {"id": 789, "name": "Test Page"},
        }

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert "💻 Code Block" in result[0].text
        assert "print('Hello World')" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_with_header(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with header content."""
        sample_block_data = {
            "id": 456,
            "content": "# Main Header",
            "uuid": "block-uuid-456",
            "properties": {},
            "children": [],
            "parent": {"id": 123},
            "page": {"id": 789, "name": "Test Page"},
        }

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert "📑 Header" in result[0].text
        assert "# Main Header" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_with_properties(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with properties."""
        sample_block_data = {
            "id": 456,
            "content": "Test content",
            "uuid": "block-uuid-456",
            "properties": {
                "important": "yes",
                "tags": ["test", "example"],
                "priority": 1,
            },
            "children": [],
            "parent": {"id": 123},
            "page": {"id": 789, "name": "Test Page"},
        }

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert "**important**: yes" in result[0].text
        assert "**tags**: test, example" in result[0].text
        assert "**priority**: 1" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_with_long_content(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with long content."""
        long_content = "This is a very long content that exceeds 500 characters. " * 20
        sample_block_data = {
            "id": 456,
            "content": long_content,
            "uuid": "block-uuid-456",
            "properties": {},
            "children": [],
            "parent": {"id": 123},
            "page": {"id": 789, "name": "Test Page"},
        }

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert "Content truncated" in result[0].text
        assert len(result[0].text) > 500  # Should be truncated

    @pytest.mark.asyncio
    async def test_get_block_content_child_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with child HTTP error."""
        sample_block_data = {
            "id": 456,
            "content": "Parent block content",
            "uuid": "block-uuid-456",
            "properties": {},
            "children": [
                ["uuid", "child-uuid-1"],
            ],
            "parent": {"id": 123},
            "page": {"id": 789, "name": "Test Page"},
        }

        # Setup mock responses
        mock_main_response = MagicMock()
        mock_main_response.status = 200
        mock_main_response.json = AsyncMock(return_value=sample_block_data)

        mock_child_response = MagicMock()
        mock_child_response.status = 500

        # Setup session mock
        mock_context1 = MagicMock()
        mock_context1.__aenter__ = AsyncMock(return_value=mock_main_response)
        mock_context1.__aexit__ = AsyncMock(return_value=None)

        mock_context2 = MagicMock()
        mock_context2.__aenter__ = AsyncMock(return_value=mock_child_response)
        mock_context2.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp_session._session_instance.post.side_effect = [
            mock_context1,
            mock_context2,
        ]

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert (
            "❌ Could not fetch child block with UUID: child-uuid-1" in result[0].text
        )

    @pytest.mark.asyncio
    async def test_get_block_content_invalid_child_reference(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with invalid child reference."""
        sample_block_data = {
            "id": 456,
            "content": "Parent block content",
            "uuid": "block-uuid-456",
            "properties": {},
            "children": [
                "invalid-child-reference",
            ],
            "parent": {"id": 123},
            "page": {"id": 789, "name": "Test Page"},
        }

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_block_data)

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "🔍 **MAIN BLOCK**" in result[0].text
        assert "❌ Invalid child reference: invalid-child-reference" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_http_error(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with HTTP error."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup session mock
        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_aiohttp_session._session_instance.post.return_value = mock_context

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "❌ Block with UUID 'block-uuid-456' not found" in result[0].text

    @pytest.mark.asyncio
    async def test_get_block_content_exception(
        self, mock_env_vars, mock_aiohttp_session
    ):
        """Test block content retrieval with exception."""
        # Setup session mock to raise exception
        mock_aiohttp_session._session_instance.post.side_effect = Exception(
            "Network error"
        )

        result = await get_block_content("block-uuid-456")

        assert len(result) == 1
        assert "❌ Error fetching block content: Network error" in result[0].text
