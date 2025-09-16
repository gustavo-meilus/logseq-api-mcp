"""Pytest configuration and shared fixtures."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(
        os.environ,
        {
            "LOGSEQ_API_ENDPOINT": "http://test-logseq:12315/api",
            "LOGSEQ_API_TOKEN": "test-token",
        },
    ):
        yield


@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp ClientSession."""
    with patch("aiohttp.ClientSession") as mock_session_class:
        # Create a mock session instance
        mock_session_instance = MagicMock()

        # Mock the session class to return our instance when used as context manager
        mock_session_class.return_value.__aenter__ = AsyncMock(
            return_value=mock_session_instance
        )
        mock_session_class.return_value.__aexit__ = AsyncMock(return_value=None)

        # Create a mock post context manager
        mock_post_context = MagicMock()

        # Make the post method return the context manager directly
        mock_session_instance.post.return_value = mock_post_context

        # Store the session instance and post context for easy access in tests
        mock_session_class._session_instance = mock_session_instance
        mock_session_class._post_context = mock_post_context

        yield mock_session_class


@pytest.fixture
def mock_successful_response():
    """Mock successful HTTP response."""
    response = MagicMock()
    response.status = 200
    response.json = AsyncMock(return_value={"success": True, "data": "test data"})
    return response


@pytest.fixture
def mock_error_response():
    """Mock error HTTP response."""
    response = MagicMock()
    response.status = 500
    response.json = AsyncMock(return_value={"error": "Internal server error"})
    return response


@pytest.fixture
def sample_page_data():
    """Sample page data for testing."""
    return {
        "id": 123,
        "uuid": "page-uuid-123",
        "originalName": "Test Page",
        "name": "Test Page",
        "journal?": False,
        "createdAt": 1640995200000,
        "updatedAt": 1640995200000,
    }


@pytest.fixture
def sample_block_data():
    """Sample block data for testing."""
    return {
        "id": 456,
        "uuid": "block-uuid-456",
        "content": "Test block content",
        "level": 1,
        "page": {"id": 123, "name": "Test Page"},
        "properties": {"status": "active"},
        "children": [],
    }
