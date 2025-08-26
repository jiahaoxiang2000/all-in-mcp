# All-in-MCP

A FastMCP-based Model Context Protocol (MCP) server providing academic paper search and PDF processing utilities. Features a modular architecture with both proxy and standalone server capabilities.

- [**Paper Tools overview _Video_**](https://www.bilibili.com/video/BV1RMKWzdEk8)
- [_Overview PDF_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/setup.pdf)

![APaper Research Direction](docs/APaper-research-direction-7x-2k-extended.gif)

## Architecture

All-in-MCP uses a modern **FastMCP architecture** with two main components:

1. **🔄 All-in-MCP Proxy Server**: Main server that routes requests to academic tools
2. **📚 APaper Module**: Isolated academic research server with specialized paper search tools

This design provides better modularity, performance, and scalability.

## Features

Both servers expose academic paper search tools as FastMCP endpoints with automatic tool registration:

### Available Tools

- **Academic Research**:
  - `search-iacr-papers`: Search academic papers from IACR ePrint Archive
  - `download-iacr-paper`: Download PDF of an IACR ePrint paper
  - `read-iacr-paper`: Read and extract text content from an IACR ePrint paper PDF
- **Bibliography Search**:
  - `search-cryptobib-papers`: Search CryptoBib bibliography database for cryptography papers (structured metadata or raw BibTeX)
- **Crossref Search**:
  - `search-crossref-papers`: Search academic papers from Crossref database
- **Google Scholar**:
  - `search-google-scholar-papers`: Search academic papers across disciplines with citation data
- **PDF Reading**:
  - `read-pdf`: Read and extract text from local and online PDF files

All tools are implemented using FastMCP decorators with automatic registration, built-in validation, and enhanced error handling.

## Quick Start

- [**Video for Env Setup**](https://www.bilibili.com/video/BV1cZKozaEjg) [**Video for Claude code**](https://www.bilibili.com/video/BV1s9KmzVEcE/)
- [_Overview PDF_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/config.pdf) [_PDF for Claude code_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/config-claude.pdf)

### Prerequisites

- Python 3.10 or higher
- UV package manager

### Installation

Install from PyPI (Recommended by `UV`)

```bash
uv pip install all-in-mcp
```

### Server Options

The main proxy server supports multiple MCP backends through environment variables:

```bash
# Run with APaper academic tools enabled
APAPER=true uv run all-in-mcp

# Run with GitHub repository tools enabled
GITHUB_REPO_MCP=true uv run all-in-mcp

# Run with both backends enabled
APAPER=true GITHUB_REPO_MCP=true uv run all-in-mcp

# Run standalone APaper server (academic tools only)
uv run apaper
```

### Integration with MCP Clients

Add the servers to your MCP client configuration:

#### VSCode Configuration

```json .vscode/mcp.json
{
  "servers": {
    "all-in-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "all-in-mcp"],
      "env": {
        "APAPER": "true",
        "GITHUB_REPO_MCP": "true"
      }
    }
  }
}
```

#### Claude Code Configuration

```json .mcp.json
{
  "mcpServers": {
    "all-in-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "all-in-mcp"],
      "env": {
        "APAPER": "true",
        "GITHUB_REPO_MCP": "true"
      }
    }
  }
}
```

## Debugging & Testing

### MCP Inspector

Use the official MCP Inspector to debug and test server functionality:

```bash
# Debug the main proxy server with APaper tools
APAPER=true npx @modelcontextprotocol/inspector uv run all-in-mcp

# Debug with all backends enabled
APAPER=true GITHUB_REPO_MCP=true npx @modelcontextprotocol/inspector uv run all-in-mcp

# Debug standalone APaper server
npx @modelcontextprotocol/inspector uv run apaper
```

The MCP Inspector provides:

- 🔍 **Interactive Tool Testing**: Test all available tools with real parameters
- 📊 **Server Information**: View server capabilities and tool schemas
- 🐛 **Debug Messages**: Monitor server communication and error messages
- ⚡ **Real-time Testing**: Execute tools and see results immediately

Perfect for development, debugging, and understanding how the FastMCP tools work.

<details>
<summary>Development</summary>

For development setup and contribution guidelines, see the [Development Guide](docs/development.md).

### Quick Development Setup

```bash
# Clone the repository
git clone https://github.com/jiahaoxiang2000/all-in-mcp.git
cd all-in-mcp

# Install with development dependencies
uv sync --extra dev

# Run tests (now using unittest)
uv run python tests/test_fastmcp_server.py
uv run python tests/test_apaper_iacr.py
uv run python tests/test_apaper_pdf.py
```

</details>
