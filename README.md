# Logseq API MCP Server

**Model Context Protocol server for Logseq API integration**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green)](https://modelcontextprotocol.io/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Tools](#available-tools)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Logseq API MCP Server provides seamless integration between [Model Context Protocol](https://modelcontextprotocol.io/) clients and [Logseq](https://logseq.com/) knowledge bases. This server enables AI assistants and other MCP clients to interact with your Logseq notes, extract educational content, and work with structured knowledge through a comprehensive set of tools.

Perfect for:

- 📚 **Educational content extraction** - Extract flashcards and study materials
- 🔍 **Knowledge base exploration** - Navigate and search through your notes
- 🎓 **Learning assistance** - AI-powered interaction with your knowledge
- 📖 **Content analysis** - Analyze relationships between pages and concepts

## Features

### Core Tools

- **Page Management** - List, explore, and analyze your Logseq pages
- **Block Operations** - Extract and work with individual note blocks
- **Link Analysis** - Discover connections between pages and concepts
- **Flashcard Extraction** - Comprehensive flashcard collection and formatting
- **Content Integration** - Complete content extraction with relationships

### Optimized for AI/LLM Consumption

- Clean, structured output formatting
- Educational content prioritization
- Hierarchical data presentation
- Emoji-enhanced readability
- Smart content truncation and organization

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- Running Logseq instance with API enabled
- Logseq API token

### Quick Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/logseq-api-mcp.git
   cd logseq-api-mcp
   ```

2. **Install dependencies with uv**

   ```bash
   uv sync
   ```

3. **Configure environment**

   ```bash
   cp .env.template .env
   # Edit .env with your Logseq API details
   ```

4. **Start the server**
   ```bash
   uv run mcp run src/server.py
   ```

## Configuration

Create a `.env` file in the project root:

```env
# Logseq API Configuration
LOGSEQ_API_ENDPOINT=http://127.0.0.1:12315/api
LOGSEQ_API_TOKEN=your_api_token_here
```

### Getting Your Logseq API Token

1. Open Logseq
2. Go to Settings → Features → Developer mode
3. Enable "HTTP APIs server"
4. Copy the displayed API token
5. Note the API endpoint (usually `http://127.0.0.1:12315/api`)

## Available Tools

| Tool                    | Description                                   | Use Case                          |
| ----------------------- | --------------------------------------------- | --------------------------------- |
| `get_all_pages`         | List all pages in your knowledge base         | Explore and navigate your content |
| `get_page_blocks`       | Get hierarchical block structure of a page    | Analyze page organization         |
| `get_page_links`        | Find all pages linking to a specific page     | Discover content relationships    |
| `get_block_content`     | Get detailed content of a specific block      | Deep-dive into specific content   |
| `get_all_page_content`  | Complete page content with relationships      | Comprehensive content analysis    |
| `get_linked_flashcards` | Extract flashcards from page and linked pages | Study and learning assistance     |

## Usage Examples

### Basic Page Exploration

```python
# List all pages in your knowledge base
all_pages = await mcp_client.call_tool("get_all_pages", {})

# Get structure of a specific page
page_blocks = await mcp_client.call_tool("get_page_blocks", {
    "page_identifier": "Machine Learning"
})

# Find pages linking to a concept
linked_pages = await mcp_client.call_tool("get_page_links", {
    "page_identifier": "Python Programming"
})
```

### Educational Content Extraction

```python
# Extract comprehensive content from a course page
course_content = await mcp_client.call_tool("get_all_page_content", {
    "page_identifier": "Data Science Course"
})

# Get all flashcards for study session
flashcards = await mcp_client.call_tool("get_linked_flashcards", {
    "page_identifier": "Linear Algebra"
})
```

### Integration with Claude Desktop

Add to your Claude Desktop MCP settings:

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

**Note:** Replace `/path/to/logseq-api-mcp` with the actual path to your cloned repository.

### Sample Output

The tools provide clean, structured output optimized for AI consumption:

```
🎯 FLASHCARDS FOR: Machine Learning Basics
📊 Found 25 flashcards across 3 pages
📄 Target page: ✅ Has flashcards | Linked pages: 12

📖 Machine Learning Basics (TARGET PAGE) (10 flashcards)

   1. ❓ Q: What is supervised learning?
      💡 A: A type of machine learning where the algorithm learns from labeled training data...
      📍 Block ID: ml-001

📖 Neural Networks (LINKED PAGE) (8 flashcards)
📖 Deep Learning (LINKED PAGE) (7 flashcards)

📈 SUMMARY:
• Total flashcards: 25
• From target page: 10
• From linked pages: 15
• Total source pages: 3
```

## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development

```bash
# Install development dependencies
uv sync --dev

# Format code
uv run ruff format

# Check code
uv run ruff check

# Test the server with inspector
uv run mcp dev src/server.py

```

### Contribution Ideas

- 🛠️ **New Tools** - Add more Logseq API integrations
- 🎨 **Output Formatting** - Improve content presentation
- 📊 **Analytics Tools** - Add knowledge base analysis features
- 🔍 **Search Enhancement** - Advanced search and filtering
- 📚 **Educational Features** - More learning-focused tools
- 🐛 **Bug Fixes** - Fix issues and improve stability

<!-- ## Roadmap

- [ ] Advanced search and filtering tools
- [ ] Batch operations for multiple pages
- [ ] Export tools (Markdown, JSON, etc.)
- [ ] Graph analysis tools
- [ ] Template and automation support
- [ ] Performance optimizations
- [ ] WebSocket support for real-time updates -->

## Documentation

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Logseq API Documentation](https://logseq.github.io/plugins/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) for the excellent protocol specification
- [Logseq](https://logseq.com/) for the amazing knowledge management platform
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) for the robust development framework

---

**Made with ❤️ for the Logseq and MCP communities**
