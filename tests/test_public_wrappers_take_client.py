"""Public tool wrappers must accept client + config as first args (v1.0.1)."""

import inspect

import pytest

from src import tools

_WRAPPERS_TO_AUDIT = [
    "get_all_pages",
    "get_all_page_content",
    "get_page_blocks",
    "get_block_content",
    "get_page_backlinks",
    "get_linked_flashcards",
    "search",
    "query",
    "find_pages_by_property",
    "get_pages_from_namespace",
    "get_pages_tree_from_namespace",
    "create_page",
    "update_page",
    "delete_page",
    "rename_page",
    "append_block_in_page",
    "insert_nested_block",
    "update_block",
    "delete_block",
    "edit_block",
    "set_block_properties",
    # Live context tools (v1.1.0)
    "get_current_page",
    "get_current_block",
    "get_editing_selection",
    "get_current_graph",
    "suggest_workspace",
]


@pytest.mark.parametrize("name", _WRAPPERS_TO_AUDIT)
def test_wrapper_first_two_params_are_client_and_config(name):
    fn = getattr(tools, name)
    sig = inspect.signature(fn)
    params = list(sig.parameters.values())
    assert params[0].name == "client"
    assert params[1].name == "config"


def test_audit_list_matches_tools_all_minus_alias():
    from src import tools

    expected = set(tools.__all__) - {"get_page_links"}
    assert set(_WRAPPERS_TO_AUDIT) == expected
