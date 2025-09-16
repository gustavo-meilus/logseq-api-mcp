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
    with patch("aiohttp.ClientSession") as mock_session:
        yield mock_session


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
