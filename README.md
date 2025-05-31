# Logseq API MCP Server

**Model Context Protocol server for Logseq API integration**

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green)](https://modelcontextprotocol.io/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![UV](https://img.shields.io/badge/package%20manager-uv-orange)](https://docs.astral.sh/uv/)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Tools](#available-tools)
- [Tool Details & Examples](#tool-details--examples)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Logseq API MCP Server provides seamless integration between [Model Context Protocol](https://modelcontextprotocol.io/) clients and [Logseq](https://logseq.com/) knowledge bases. This server enables AI assistants and other MCP clients to interact with your Logseq notes, extract educational content, analyze knowledge relationships, and work with structured information through a comprehensive set of 6 specialized tools.

Perfect for:

- 📚 **Educational Content Management** - Extract and organize flashcards and study materials
- 🎓 **Learning Systems** - Build AI-powered study assistants and spaced repetition tools
- 🔍 **Knowledge Base Analysis** - Discover relationships and patterns in your notes
- 📊 **Content Discovery** - Navigate complex knowledge graphs with AI assistance
- 🧠 **Academic Research** - Analyze course materials and learning resources

## Features

### 🛠️ Core Tools (6 Total)

1. **`get_all_pages`** - Complete page listing with metadata
2. **`get_page_blocks`** - Hierarchical block structure analysis
3. **`get_page_links`** - Page relationship and reference discovery
4. **`get_block_content`** - Detailed block content with children
5. **`get_all_page_content`** - Comprehensive page content extraction
6. **`get_linked_flashcards`** - Advanced flashcard collection and analysis

### 🎯 Optimized for AI/LLM Consumption

- **Clean Structured Output** - Emoji-enhanced, hierarchical formatting
- **Educational Content Focus** - Specialized flashcard and learning material extraction
- **Comprehensive Metadata** - Block IDs, UUIDs, timestamps, properties, and relationships
- **Smart Content Organization** - Automatic categorization and summary generation
- **Language Agnostic** - Works with any Logseq knowledge base language

## Installation

### Prerequisites

- **Python 3.11+** - Modern Python with async/await support
- **[uv](https://docs.astral.sh/uv/)** - Fast Python package manager and project management
- **Running Logseq instance** with API enabled
- **Logseq API token** for authentication

### Quick Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/gustavo-meilus/logseq-api-mcp.git
   cd logseq-api-mcp
   ```

2. **Install with uv**

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

1. Open Logseq application
2. Go to **Settings → Features → Developer mode**
3. Enable **"HTTP APIs server"**
4. Copy the displayed API token
5. Note the API endpoint (default: `http://127.0.0.1:12315/api`)
6. Activate the API

## Available Tools

| Tool                    | Description                             | Output                               | Best For                       |
| ----------------------- | --------------------------------------- | ------------------------------------ | ------------------------------ |
| `get_all_pages`         | Lists all pages with essential metadata | 568 pages (135 journal, 433 regular) | Navigation, page discovery     |
| `get_page_blocks`       | Hierarchical block tree structure       | Multi-level tree with IDs, UUIDs     | Structure analysis, navigation |
| `get_page_links`        | Pages linking to target page            | Reference analysis with metadata     | Relationship discovery         |
| `get_block_content`     | Detailed block info with children       | Block content + immediate children   | Deep content analysis          |
| `get_all_page_content`  | Complete page content + references      | Full content with linked sources     | Comprehensive content review   |
| `get_linked_flashcards` | Flashcards from page + linked pages     | 20 flashcards across 2 pages         | Study material extraction      |

## Tool Details & Examples

### 🗂️ `get_all_pages`

**Purpose:** Get a clean listing of all pages in your knowledge base

**Output Format:**

```
📊 LOGSEQ PAGES LISTING
📈 Total pages: 568
📅 Journal pages: 135
📄 Regular pages: 433

📄 REGULAR PAGES:
📄 Domain Driven Design (DDD) I | ID: 3460 | UUID: 682cfd19-7df6-46e0-a6f3-c09eca3b2530
📄 MBA Engenharia de Software | ID: 170 | UUID: 682fa28c-a3cc-47f2-ae65-7b7db57e1d67
```

**Use Cases:**

- Knowledge base exploration
- Page inventory and organization
- Finding specific pages by name or metadata

---

### 🌳 `get_page_blocks`

**Purpose:** Get hierarchical block structure of any page

**Example Input:** `"Domain Driven Design (DDD) I"`

**Output Features:**

- Tree structure with indentation levels
- Block IDs, UUIDs, and parent-child relationships
- Property extraction and metadata
- Multi-level hierarchy support (up to 8+ levels)

**Sample Output:**

```
🌳 PAGE BLOCKS TREE STRUCTURE
📄 Page: Domain Driven Design (DDD) I (ID: 3460)
📊 Total blocks: 1

📋 tipo:: #aula curso:: [[MBA Engenharia de Software]]
   📊 ID:3544 | UUID:682cfd19-2826-46b7-8222-0821b11abc60 | Level:1
   👇 Children: 7

  H1 # Flashcards [heading: 1]
     📊 ID:3552 | UUID:682cfd19-4c9c-40dd-8cb1-c2625315b8ae | Level:2
     👇 Children: 10
```

---

### 🔗 `get_page_links`

**Purpose:** Find all pages that link to a target page

**Example Result for "Domain Driven Design (DDD) I":**

```
🔗 PAGE LINKS ANALYSIS
📄 Target Page: Domain Driven Design (DDD) I
📊 Found 1 pages linking to this page

📄 1. Domain Driven Design (DDD) II
   🔑 ID: 3588 | UUID: 682cfd19-3a24-4636-a5d5-c62ea57d352e
   📊 References: 1 | Journal: No
   ⚙️ Properties: relacionado: Domain Driven Design (DDD) I
```

**Applications:**

- Discover related content and cross-references
- Build knowledge maps and relationship graphs
- Find course sequences and learning paths

---

### 🔍 `get_block_content`

**Purpose:** Get detailed information about a specific block and its immediate children

**Example Input:** UUID `682cfd19-3c3f-427c-a0be-c5a3a197ea20`

**Output:**

```
🔍 MAIN BLOCK
📌 Block ID: 3465
🔑 UUID: 682cfd19-3c3f-427c-a0be-c5a3a197ea20

📝 CONTENT:
💡 Flashcard
Por que o DDD prioriza a colaboração entre desenvolvedores e especialistas do domínio? #card
+ [ ] Porque os especialistas do domínio são responsáveis apenas por aprovar a infraestrutura tecnológica.
+ [ ] Para garantir que o software seja construído com base no conhecimento profundo do domínio, reduzindo ambiguidades e erros.

👶 IMMEDIATE CHILDREN:
🔸 CHILD 1:
Resposta Correta: Para garantir que o software seja construído com base no conhecimento profundo do domínio, reduzindo ambiguidades e erros.
```

---

### 📖 `get_all_page_content`

**Purpose:** Extract comprehensive content from a page including properties, blocks, and linked references

**Key Features:**

- Complete hierarchical content structure
- Property extraction and formatting
- Flashcard identification and extraction
- Linked references analysis
- Educational content optimization

**Example Summary:**

```
📖 Domain Driven Design (DDD) I
📊 1 blocks | 1 linked sources

📄 COMPREHENSIVE CONTENT:
📄 Page Properties [3544]
   📋 curso: MBA Engenharia de Software | tipo: aula | professor: Guilherme Bezerra de Lima

🎯 # Flashcards [3552]
   💡 Flashcard [3465]
      ❓ Q: Por que o DDD prioriza a colaboração entre desenvolvedores e especialistas do domínio?
```

---

### 🧠 `get_linked_flashcards`

**Purpose:** Comprehensive flashcard extraction from target page and all linked pages

**Real Example Results for "Domain Driven Design (DDD) I":**

```
🎯 LINKED FLASHCARDS ANALYSIS
📄 Target Page: Domain Driven Design (DDD) I
🔗 Searched 2 pages (target + 1 linked)
💡 Found 20 flashcards total

📚 Domain Driven Design (DDD) I (10 flashcards)
📚 Domain Driven Design (DDD) II (10 flashcards)

📊 SUMMARY:
• Total flashcards: 20
• Total answer blocks: 0
• Pages with flashcards: 2
• Average answers per flashcard: 0.0
```

**Advanced Features:**

- Multi-choice question support
- Answer block extraction and linking
- Cross-page flashcard discovery
- Educational metadata preservation
- Learning system integration ready

## Usage Examples

Add to your Claude Desktop MCP settings (`~/.claude/claude_desktop_config.json`):

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

## Development

### Project Structure

```
logseq-api-mcp/
├── src/
│   ├── server.py              # MCP server implementation
│   ├── registry.py            # Tool registry and configuration
│   └── tools/                 # Tool implementations
│       ├── __init__.py        # Tool exports
│       ├── get_all_pages.py   # Page listing tool
│       ├── get_page_blocks.py # Block structure tool
│       ├── get_page_links.py  # Page links tool
│       ├── get_block_content.py # Block detail tool
│       ├── get_all_page_content.py # Complete content tool
│       └── get_linked_flashcards.py # Flashcard extraction tool
├── pyproject.toml             # UV project configuration
├── .env.template              # Environment template
└── README.md                  # This file
```

### Development Setup

```bash
# Install with development dependencies
uv sync --dev

# Format code (auto-fixes issues)
uv run ruff check --fix && uv run ruff format

# Test server with MCP inspector
uv run mcp dev src/server.py

# Run server directly
uv run mcp run src/server.py
```

### Code Quality Standards

- **Python 3.11+** with modern async/await patterns
- **PEP 8** compliance via Ruff formatting
- **Type hints** for better IDE support
- **Error handling** with comprehensive exception management
- **Environment variables** for configuration
- **Modular design** with separate tool implementations

## Contributing

We follow **GitHub Flow** for all contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for complete details.

### Quick Start

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/add-search-tool
   ```
3. **Make your changes**
4. **Format and check code**
   ```bash
   uv run ruff check --fix && uv run ruff format
   ```
5. **Test your changes**
   ```bash
   uv run mcp dev src/server.py
   ```
6. **Commit your changes**
   ```bash
   git commit -m "feat: add new search tool"
   ```
7. **Push to your branch**
   ```bash
   git push origin feature/add-search-tool
   ```
8. **Open a Pull Request**

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation

### Commit Messages

Follow conventional commits:

- `feat: add new search tool`
- `fix: resolve API timeout issue`
- `docs: update installation guide`

## Documentation & Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Logseq API Documentation](https://logseq.github.io/plugins/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [UV Package Manager](https://docs.astral.sh/uv/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) for the excellent protocol specification
- [Logseq](https://logseq.com/) for the powerful knowledge management platform
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) for the robust development framework
- [UV](https://docs.astral.sh/uv/) for modern Python package management

---

**Made for the Logseq and MCP communities**
