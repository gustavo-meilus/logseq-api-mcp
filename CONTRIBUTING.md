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
# Make changes - create your tool file (no imports needed!)
# Example: src/tools/search_tool.py

# Format and check code
uv run ruff check --fix && uv run ruff format

# Test changes (automated testing)
uv run python tests/test_mcp_server.py

# Test with MCP Inspector (manual verification)
uv run mcp dev src/server.py

# Commit frequently
git add .
git commit -m "feat: add search functionality for content discovery"
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

## Adding New Tools (Super Simple!)

Thanks to our **dynamic tool discovery system**, adding tools is incredibly easy:

### 1. Create Tool File

Create `src/tools/your_tool.py`:

```python
def your_tool(param: str) -> dict:
    """
    Your tool description.

    Args:
        param: Input parameter description

    Returns:
        Dict with tool results
    """
    return {
        "result": f"Processed: {param}",
        "status": "success"
    }
```

### 2. That's It! 🎉

The system automatically:

- ✅ **Discovers** your tool
- ✅ **Imports** the function
- ✅ **Registers** with MCP server
- ✅ **Validates** in CI tests

### Tool Guidelines

- **Location**: Must be in `src/tools/` directory
- **Naming**: Don't start with `_` (files or functions)
- **Documentation**: Include comprehensive docstrings
- **Type Hints**: Use for all parameters and returns
- **Error Handling**: Include proper exception management
- **Testing**: Tools are automatically tested by CI

## Testing Framework

### Automated Testing

Our testing system validates the dynamic discovery:

```bash
# Run all tests
uv run python tests/test_mcp_server.py
```

**What gets tested:**

- ✅ **Server Health** - MCP server starts correctly
- ✅ **Tool Discovery** - All tools auto-discovered
- ✅ **Registration** - Tools properly registered
- ✅ **Integration** - End-to-end functionality

### Test Output

```
🔍 Testing MCP Server Health and Tools...
🔧 Discovered tools (auto-discovery): ['get_all_pages', 'your_new_tool', ...]

🏥 Testing server health...
✅ Server started and responded successfully
✅ Dynamic tool discovery working correctly

🎉 MCP Server test completed successfully!
   📊 Tools auto-discovered: 7
   🏥 Server health: OK
   🔄 Dynamic discovery: OK
```

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
- **Testing**: Automated validation via CI

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

# Run automated tests
uv run python tests/test_mcp_server.py
```

## Dynamic Discovery Architecture

### How It Works

1. **`src/tools/__init__.py`**:

   - Scans `src/tools/` directory for `.py` files
   - Dynamically imports all public functions
   - Populates `__all__` list automatically

2. **`src/registry.py`**:

   - Imports `tools` module
   - Iterates through `tools.__all__`
   - Auto-registers each tool with MCP server

3. **`tests/test_mcp_server.py`**:
   - Validates tool discovery works
   - Ensures server health
   - Confirms all tools are registered

### Development Flow

```
Tool File Creation → Auto-Discovery → Import → Registration → CI Validation
```

### Benefits

- **Zero Maintenance**: No manual imports/registrations
- **Error Prevention**: Can't forget to register tools
- **Instant Integration**: New tools work immediately
- **CI Protection**: Tests catch any issues

## Troubleshooting

### Tool Not Discovered

- Ensure file is in `src/tools/` directory
- Function name shouldn't start with `_`
- File name shouldn't start with `_`
- Check for syntax/import errors

### Test Failures

- Run `uv run python tests/test_mcp_server.py` locally
- Check server logs for errors
- Verify Logseq API is accessible
- Ensure environment variables are set

### Server Issues

- Test manually: `uv run mcp dev src/server.py`
- Check `.env` configuration
- Verify Logseq API token is valid

## Commit Messages

Follow conventional commits:

- `feat: add new search tool`
- `fix: resolve API timeout issue`
- `docs: update installation guide`
- `refactor: improve error handling`

## Example Contribution

Here's a complete example of adding a new tool:

### 1. Create Tool

`src/tools/count_pages.py`:

```python
from typing import Dict, Any

def count_pages() -> Dict[str, Any]:
    """
    Count total pages in the knowledge base.

    Returns:
        Dict with page count information
    """
    # Implementation here
    return {
        "total_pages": 42,
        "status": "success"
    }
```

### 2. Test Locally

```bash
# Test discovery
uv run python tests/test_mcp_server.py

# Test manually
uv run mcp dev src/server.py
```

### 3. Commit & Push

```bash
git add src/tools/count_pages.py
git commit -m "feat: add page counting tool"
git push origin feature/add-page-counter
```

### 4. Open PR

- Tool is automatically discovered
- CI tests validate integration
- Ready for review!

## Questions?

- Check existing issues and discussions
- Create new issue for bugs/features
- Join community discussions
- Review the [README.md](README.md) for more details
