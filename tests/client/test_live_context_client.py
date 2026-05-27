"""Tests for LiveContextClient methods on LogseqClient."""

from unittest.mock import AsyncMock, patch

import pytest

from src.client.config import LogseqConfig
from src.client.logseq_client import LogseqClient


@pytest.fixture
def config():
    return LogseqConfig(endpoint="http://localhost:12315/api", token="test-tok")


@pytest.fixture
def client(config):
    return LogseqClient(config)


@pytest.fixture
def mock_call(client):
    with patch.object(client, "_call", new_callable=AsyncMock) as mock:
        yield mock


# ── get_current_page ─────────────────────────────────────────────────────────


async def test_get_current_page_calls_correct_method(client, mock_call):
    mock_call.return_value = {"name": "My Page", "uuid": "abc"}
    result = await client.get_current_page()
    mock_call.assert_awaited_once_with("logseq.Editor.getCurrentPage")
    assert result["name"] == "My Page"


async def test_get_current_page_returns_none_when_no_active_page(client, mock_call):
    mock_call.return_value = None
    result = await client.get_current_page()
    assert result is None


# ── get_current_block ─────────────────────────────────────────────────────────


async def test_get_current_block_calls_correct_method(client, mock_call):
    mock_call.return_value = {"uuid": "block-1", "content": "some content"}
    result = await client.get_current_block()
    mock_call.assert_awaited_once_with("logseq.Editor.getCurrentBlock")
    assert result["content"] == "some content"


async def test_get_current_block_returns_none_when_no_editing(client, mock_call):
    mock_call.return_value = None
    result = await client.get_current_block()
    assert result is None


# ── get_editing_selection ─────────────────────────────────────────────────────


async def test_get_editing_selection_calls_correct_method(client, mock_call):
    mock_call.return_value = [
        {"uuid": "b1", "content": "block 1"},
        {"uuid": "b2", "content": "block 2"},
    ]
    result = await client.get_editing_selection()
    mock_call.assert_awaited_once_with("logseq.Editor.getEditingBlockSelection")
    assert len(result) == 2


async def test_get_editing_selection_returns_empty_list_on_none(client, mock_call):
    mock_call.return_value = None
    result = await client.get_editing_selection()
    assert result == []


# ── get_current_graph ─────────────────────────────────────────────────────────


async def test_get_current_graph_calls_correct_method(client, mock_call):
    mock_call.return_value = {
        "name": "my-notes",
        "path": "/Users/me/Documents/my-notes",
        "url": "logseq://graph/my-notes",
    }
    result = await client.get_current_graph()
    mock_call.assert_awaited_once_with("logseq.App.getCurrentGraph")
    assert result["path"] == "/Users/me/Documents/my-notes"


async def test_get_current_graph_returns_empty_dict_on_none(client, mock_call):
    mock_call.return_value = None
    result = await client.get_current_graph()
    assert result == {}
