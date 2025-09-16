.PHONY: fix format check test install

# Fix code formatting and linting issues
fix:
	@echo "🔧 Running Ruff fix and format..."
	uv run ruff check src/ tests/ --fix
	uv run ruff format src/ tests/
	@echo "✅ Code fixed and formatted!"

# Format code only
format:
	@echo "🎨 Formatting code..."
	uv run ruff format src/ tests/
	@echo "✅ Code formatted!"

# Check code quality
check:
	@echo "🔍 Checking code quality..."
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/
	@echo "✅ Code quality checks passed!"

# Run tests
test:
	@echo "🧪 Running tests..."
	uv run pytest tests/ -v

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	uv sync --dev

# Install pre-commit hooks
install-hooks:
	@echo "🪝 Installing pre-commit hooks..."
	uv run pre-commit install

# Run all checks
all: check test
	@echo "✅ All checks passed!"
