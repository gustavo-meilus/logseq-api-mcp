# Contributing to Logseq API MCP

## GitHub Flow Process

We follow **GitHub Flow** for all contributions:

### 1. Create Feature Branch

```bash
# Sync with latest main
git checkout main
git pull origin main

# Create descriptive branch
git checkout -b feature/add-search-tool
git checkout -b fix/api-timeout-issue
git checkout -b docs/update-installation
```

### 2. Development Process

```bash
# Make changes
# Edit files...

# Format and check code
uv run ruff check --fix && uv run ruff format

# Test changes
uv run mcp dev src/server.py

# Commit frequently
git add .
git commit -m "Add search functionality for blocks"
git push origin feature/add-search-tool
```

### 3. Pull Request

- Open PR **early** for feedback
- Use the provided PR template
- Ensure all CI checks pass
- Request review from maintainers

### 4. Code Review

- Address feedback promptly
- Push additional commits as needed
- Maintain clean commit history

### 5. Merge to Main

- Squash and merge after approval
- Delete feature branch
- `main` branch triggers deployment

## Branch Naming Conventions

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring
- `test/description` - Test improvements

## Quality Standards

- **Code formatting**: `ruff check --fix && ruff format`
- **Type hints**: Use for all functions
- **Docstrings**: Required for all functions/classes
- **Error handling**: Comprehensive exception management
- **Testing**: Manual MCP server testing

## Development Setup

```bash
# Clone and setup
git clone https://github.com/gustavo-meilus/logseq-api-mcp.git
cd logseq-api-mcp
uv sync

# Environment setup
cp .env.template .env
# Edit .env with your Logseq API details

# Test installation
uv run mcp dev src/server.py
```

## Commit Messages

Follow conventional commits:

- `feat: add new search tool`
- `fix: resolve API timeout issue`
- `docs: update installation guide`
- `refactor: improve error handling`
