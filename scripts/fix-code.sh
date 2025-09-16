#!/bin/bash

# Fix code formatting and linting issues
echo "🔧 Running Ruff fix and format..."

# Run Ruff fix
uv run ruff check src/ tests/ --fix

# Run Ruff format
uv run ruff format src/ tests/

echo "🔍 Running MyPy type check..."

# Run MyPy type check
uv run mypy src/ --ignore-missing-imports --show-error-codes

echo "✅ Code fixed and formatted!"
