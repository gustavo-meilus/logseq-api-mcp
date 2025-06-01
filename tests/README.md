# MCP Server Tests

This directory contains tests for the Logseq API MCP server.

## Test Structure

### `test_mcp_server.py`

The main test script that validates:

1. **Server Health**: Ensures the MCP server starts and runs correctly
2. **Dynamic Discovery**: Verifies the automatic tool discovery system works
3. **Auto-Registration**: Confirms all discovered tools are properly registered

## How It Works

### Dynamic Tool Discovery

The system automatically discovers tools by:

1. **Auto-Scan**: Scanning `src/tools/` directory for Python files
2. **Function Detection**: Finding all public functions in each module
3. **Auto-Import**: Dynamically importing and registering discovered tools
4. **Zero Configuration**: No manual imports or registrations needed

### Server Health Check

The test uses the `mcp dev` command to:

1. Start the MCP server
2. Let it run for a few seconds (timeout expected)
3. Verify it doesn't crash on startup

## Running Tests

### Locally

```bash
uv run python tests/test_mcp_server.py
```

### In CI

The test runs automatically in GitHub Actions as part of the CI pipeline.

## Adding New Tools

Adding a new tool is now **completely automatic**:

1. **Create** `src/tools/your_new_tool.py` with your function:

   ```python
   def your_new_tool(param: str) -> dict:
       """Your tool description."""
       return {"result": f"processed {param}"}
   ```

2. **That's it!** The system automatically:
   - Discovers the tool
   - Imports the function
   - Registers it with the MCP server
   - Validates it in tests

## Test Output

Example successful run:

```
🔍 Testing MCP Server Health and Tools...
🔧 Discovered tools (auto-discovery): ['get_all_pages', 'get_version', 'ping', ...]

🏥 Testing server health...
✅ Server started and responded successfully
✅ Dynamic tool discovery working correctly

🎉 MCP Server test completed successfully!
   📊 Tools auto-discovered: 8
   🏥 Server health: OK
   🔄 Dynamic discovery: OK
```

## Dynamic System Benefits

- **Zero Maintenance**: No need to update imports or registrations
- **Auto-Discovery**: New tools are automatically detected
- **Consistent**: All tools follow the same discovery pattern
- **Error-Free**: No risk of forgetting to register tools

## Troubleshooting

### Tool Not Discovered

If your tool isn't found:

1. Ensure the file is in `src/tools/` directory
2. Function name shouldn't start with `_`
3. File name shouldn't start with `_`
4. Check for import errors in the tool module

### Server Startup Errors

If the server fails to start:

1. Check for syntax errors in your tool functions
2. Verify all imports in tool files are correct
3. Run the server manually: `uv run mcp dev src/server.py`

## Architecture

### `src/tools/__init__.py`

- Automatically scans the tools directory
- Dynamically imports all tool modules
- Populates `__all__` with discovered functions
- Makes tools available for import

### `src/registry.py`

- Imports the tools module
- Iterates through `tools.__all__`
- Automatically registers each tool with the MCP server

### Dynamic Flow

```
Tool File → Auto-Discovery → Import → Registration → Validation
```

## Future Enhancements

This framework can be extended to:

- Add metadata-based tool configuration
- Implement tool categories/grouping
- Add automatic API documentation generation
- Support tool dependencies and ordering
- Performance testing and profiling
