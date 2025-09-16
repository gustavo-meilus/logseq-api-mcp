"""
Comprehensive test runner for all Logseq API MCP server tools.
"""

import sys
from pathlib import Path

import pytest

# Add src to path so we can import tools
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def run_all_tests():
    """Run all tests with coverage."""
    # Run pytest with coverage
    pytest_args = [
        "tests/",
        "-v",  # verbose
        "--tb=short",  # short traceback format
        "--cov=src/tools",  # coverage for tools directory
        "--cov-report=term-missing",  # show missing lines
        "--cov-report=html",  # generate HTML report
        "--cov-fail-under=90",  # fail if coverage is below 90%
    ]

    return pytest.main(pytest_args)


def run_specific_tool_tests(tool_name):
    """Run tests for a specific tool."""
    test_file = f"tests/test_{tool_name}.py"
    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        return 1

    pytest_args = [
        test_file,
        "-v",
        "--tb=short",
        f"--cov=src/tools/{tool_name}.py",
        "--cov-report=term-missing",
    ]

    return pytest.main(pytest_args)


def main():
    """Main test runner."""
    import argparse

    parser = argparse.ArgumentParser(description="Run Logseq API MCP server tests")
    parser.add_argument(
        "--tool",
        help="Run tests for a specific tool only",
        choices=[
            "append_block_in_page",
            "create_page",
            "edit_block",
            "get_tools",
        ],
    )
    parser.add_argument(
        "--no-coverage", action="store_true", help="Run tests without coverage"
    )

    args = parser.parse_args()

    if args.tool:
        print(f"🧪 Running tests for {args.tool}...")
        return run_specific_tool_tests(args.tool)
    else:
        print("🧪 Running all tests...")
        if args.no_coverage:
            pytest_args = ["tests/", "-v", "--tb=short"]
            return pytest.main(pytest_args)
        else:
            return run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
