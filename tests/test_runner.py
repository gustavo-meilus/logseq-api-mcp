"""Test runner for individual tool testing."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest


def run_tool_tests(tool_name: str = None):
    """Run tests for a specific tool or all tools."""
    if tool_name:
        test_file = f"tests/test_{tool_name}.py"
        if Path(test_file).exists():
            pytest.main([test_file, "-v"])
        else:
            print(f"Test file {test_file} not found")
    else:
        # Run all tests
        pytest.main(["tests/", "-v"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run tool tests")
    parser.add_argument("--tool", help="Specific tool to test")
    args = parser.parse_args()

    run_tool_tests(args.tool)
