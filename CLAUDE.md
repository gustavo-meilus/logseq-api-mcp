# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Model Context Protocol (MCP) server** that provides AI assistants with seamless access to Logseq knowledge bases. The project features a sophisticated **dynamic tool discovery system** that automatically detects, imports, and registers any new tools added to the codebase without requiring manual configuration.

**Key Innovation**: Zero-configuration tool management - simply add a Python file to `src/tools/` and it's automatically available.

## Core Architecture

### Dynamic Tool Discovery System

The project's central innovation is its automatic tool management:

1. **`src/tools/__init__.py`**: Scans the tools directory, dynamically imports all Python files, and populates `__all__` with discovered functions
2. **`src/registry.py`**: Imports the tools module and automatically registers each discovered tool with the MCP server
3. **`src/server.py`**: Simple FastMCP server that uses the registry to make all tools available

**Flow**: `Tool File → Auto-Discovery → Import → Registration → Validation`

### Tool Structure

Each tool in `src/tools/` is a standalone Python module with one or more functions that become MCP tools. Tools follow this pattern:
- Located in `src/tools/` directory
- Function names don't start with `_`
- Include comprehensive docstrings
- Use type hints
- Handle Logseq API authentication via environment variables

## Development Commands

### Installation & Setup
```bash
# Install dependencies (uses UV package manager)
uv sync

# Install with development dependencies
uv sync --dev

# Copy environment template and configure
cp .env.template .env
# Edit .env with your Logseq API details
```

### Running the Server
```bash
# Start MCP server
uv run mcp run src/server.py

# Development mode with MCP inspector
uv run mcp dev src/server.py
```

### Testing
```bash
# Run comprehensive test suite
uv run python tests/test_mcp_server.py

# The test validates:
# - Server health and startup
# - Dynamic tool discovery functionality
# - Tool registration completeness
```

### Code Quality
```bash
# Format and lint code (uses Ruff)
uv run ruff check --fix && uv run ruff format
```

## Adding New Tools

The dynamic discovery system makes adding tools incredibly simple:

### 1. Create Tool File
Create `src/tools/your_tool_name.py`:

```python
import os
import aiohttp
from typing import List
from mcp.types import TextContent
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

async def your_tool_name(param: str) -> List[TextContent]:
    """
    Tool description here.
    
    Args:
        param: Description of parameter
        
    Returns:
        List of TextContent with results
    """
    endpoint = os.getenv("LOGSEQ_API_ENDPOINT", "http://127.0.0.1:12315/api")
    token = os.getenv("LOGSEQ_API_TOKEN", "auth")
    
    # Implementation here
    return [TextContent(type="text", text="Your formatted output")]
```

### 2. That's It!
The system automatically:
- Discovers your tool file
- Imports the function
- Registers it with the MCP server
- Validates it in CI tests

**No manual imports, registrations, or configuration needed.**

## Environment Configuration

### Required Environment Variables
```env
# Logseq API Configuration
LOGSEQ_API_ENDPOINT=http://127.0.0.1:12315/api
LOGSEQ_API_TOKEN=your_api_token_here
```

### Getting Logseq API Token
1. Open Logseq application
2. Go to **Settings → Features → Developer mode**
3. Enable **"HTTP APIs server"**
4. Copy the displayed API token
5. Note the API endpoint (default: `http://127.0.0.1:12315/api`)

## Existing Tools Architecture

The project includes 6 core tools that demonstrate different patterns:

- **`get_all_pages`**: Simple listing with metadata
- **`get_page_blocks`**: Hierarchical tree structure analysis
- **`get_page_links`**: Relationship discovery between pages
- **`get_block_content`**: Detailed block content with children
- **`get_all_page_content`**: Comprehensive page extraction
- **`get_linked_flashcards`**: Advanced cross-page content analysis

All tools follow consistent patterns:
- Async functions returning `List[TextContent]`  
- Environment-based API configuration
- Emoji-enhanced, structured output for AI consumption
- Comprehensive error handling with aiohttp sessions

## Testing Strategy

### Automated Testing
The testing system validates the dynamic discovery architecture:

```bash
uv run python tests/test_mcp_server.py
```

**What gets tested:**
- Server starts without errors
- Dynamic tool discovery finds all tools
- All discovered tools are properly registered
- Server responds to MCP protocol correctly

### Test Output
```
🔍 Testing MCP Server Health and Tools...
🔧 Discovered tools (auto-discovery): ['get_all_pages', 'get_page_blocks', ...]

🏥 Testing server health...
✅ Server started and responded successfully
✅ Dynamic tool discovery working correctly

🎉 MCP Server test completed successfully!
   📊 Tools auto-discovered: 6
   🏥 Server health: OK
   🔄 Dynamic discovery: OK
```

## Key Dependencies & Technologies

- **Python 3.11+**: Modern async/await support required
- **UV**: Fast Python package manager for dependency management
- **FastMCP**: MCP server implementation from the official Python SDK
- **aiohttp**: Async HTTP client for Logseq API calls
- **Ruff**: Code formatting and linting
- **dotenv**: Environment variable management

## MCP Integration

### Claude Desktop Configuration
Add to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "logseq-api": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/logseq-api-mcp",
        "python",
        "src/server.py"
      ],
      "env": {
        "LOGSEQ_API_ENDPOINT": "http://127.0.0.1:12315/api",
        "LOGSEQ_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Development Guidelines

### Code Patterns
- All API calls use async/await with aiohttp
- Environment variables loaded from project root `.env`
- Consistent error handling and logging
- Emoji-enhanced output formatting for AI readability
- Type hints for all function signatures

### Tool Requirements
- Must be in `src/tools/` directory
- Function names cannot start with `_`
- File names cannot start with `_`
- Include comprehensive docstrings
- Use proper type hints
- Handle exceptions gracefully

### Quality Standards
- **Ruff formatting**: `uv run ruff check --fix && uv run ruff format`
- **Type safety**: Full type hints for parameters and returns
- **Documentation**: Comprehensive docstrings for all functions
- **Testing**: Automatic validation via dynamic discovery tests

## Architecture Benefits

### Zero Configuration Management
- **No Manual Imports**: Tools are automatically discovered and imported
- **No Registration Code**: Registry handles all tool registration automatically  
- **No Maintenance Overhead**: Adding tools requires zero configuration changes
- **Error Prevention**: Impossible to forget to register new tools

### Scalability
- **Plugin Architecture**: Easy to extend with new Logseq API capabilities
- **Consistent Patterns**: All tools follow the same discovery and registration flow
- **CI Validation**: Automated testing ensures all tools work correctly
- **Development Velocity**: New tools are immediately available without configuration

This architecture demonstrates how dynamic discovery patterns can eliminate configuration overhead while maintaining robust testing and validation.