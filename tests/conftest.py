"""
Pytest configuration and shared fixtures for Logseq API MCP server tests.
"""

import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientResponse

# Add src to path so we can import tools
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


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
    """Mock aiohttp ClientSession for testing."""
    with patch("aiohttp.ClientSession") as mock_session:
        # Create a proper async context manager mock
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock()
        mock_context.__aexit__ = AsyncMock()
        mock_session.return_value = mock_context
        yield mock_session


@pytest.fixture
def mock_successful_response():
    """Mock successful HTTP response."""
    mock_response = MagicMock(spec=ClientResponse)
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value={"success": True, "id": "123", "uuid": "test-uuid"}
    )
    return mock_response


@pytest.fixture
def mock_error_response():
    """Mock error HTTP response."""
    mock_response = MagicMock(spec=ClientResponse)
    mock_response.status = 500
    mock_response.json = AsyncMock(return_value={"error": "Internal server error"})
    return mock_response


@pytest.fixture
def mock_empty_response():
    """Mock empty response."""
    mock_response = MagicMock(spec=ClientResponse)
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=None)
    return mock_response


@pytest.fixture
def sample_page_data():
    """Sample page data for testing."""
    return {
        "id": 123,
        "uuid": "page-uuid-123",
        "name": "Test Page",
        "originalName": "Test Page",
        "journal?": False,
        "format": "markdown",
        "properties": {"status": "active", "priority": "high"},
        "updatedAt": 1640995200000,
    }


@pytest.fixture
def sample_block_data():
    """Sample block data for testing."""
    return {
        "id": 456,
        "uuid": "block-uuid-456",
        "content": "This is a test block",
        "page": {"id": 123, "name": "Test Page"},
        "parent": {"id": 0},
        "level": 1,
        "properties": {"type": "note"},
        "children": [],
    }


@pytest.fixture
def sample_flashcard_data():
    """Sample flashcard data for testing."""
    return {
        "id": 789,
        "uuid": "card-uuid-789",
        "content": "What is the capital of France? #card",
        "page": {"id": 123, "name": "Geography"},
        "properties": {"card-last-interval": 1, "card-repeats": 3},
    }


@pytest.fixture
def mock_logseq_api_call():
    """Mock Logseq API call with configurable response."""

    def _mock_call(response_data=None, status_code=200, side_effect=None):
        mock_response = MagicMock(spec=ClientResponse)
        mock_response.status = status_code
        if side_effect:
            mock_response.json = AsyncMock(side_effect=side_effect)
        else:
            mock_response.json = AsyncMock(return_value=response_data)
        return mock_response

    return _mock_call


@pytest.fixture
def mock_dotenv_load():
    """Mock dotenv load_dotenv function."""
    with patch("dotenv.load_dotenv") as mock_load:
        yield mock_load
