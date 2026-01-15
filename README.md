# All-in-MCP

A FastMCP-based Model Context Protocol (MCP) server providing academic paper search, web search, and PDF processing utilities. Features a modular architecture with both proxy and standalone server capabilities.

- [_All-in-MCP Introduction Slides_](docs/slide/intro.pdf)
- [**Introduction Video on Bilibili**](https://www.bilibili.com/video/BV1ZcvNzSEX5/)

<details>
<summary>APaper Module Introduction</summary>

- [**Paper Tools overview _Video_**](https://www.bilibili.com/video/BV1RMKWzdEk8)
- [_Overview PDF_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/setup.pdf)

![APaper Research Direction](docs/APaper-research-direction-7x-2k-extended.gif)

</details>

## Architecture

All-in-MCP uses a modern **FastMCP architecture** with three main components:

1. **🔄 All-in-MCP Proxy Server**: Main server that routes requests to academic tools and web search
2. **📚 APaper Module**: Isolated academic research server with specialized paper search tools
3. **🔍 Qwen Search Module**: Web search server powered by Qwen/Dashscope API with SSE-based MCP

This design provides better modularity, performance, and scalability.

## Features

All servers expose search tools as FastMCP endpoints with automatic tool registration:

### Available Tools

| Category                  | Tool Name                               | Description                                                    | Backend         |
| ------------------------- | --------------------------------------- | -------------------------------------------------------------- | --------------- |
| **Academic Research**     | `apaper_search_iacr_papers`             | Search academic papers from IACR ePrint Archive                | APaper          |
|                           | `apaper_download_iacr_paper`            | Download PDF of an IACR ePrint paper                           | APaper          |
|                           | `apaper_read_iacr_paper`                | Read and extract text content from an IACR ePrint paper PDF    | APaper          |
| **Bibliography Search**   | `apaper_search_dblp_papers`             | Search DBLP computer science bibliography database             | APaper          |
| **Cross-platform Search** | `apaper_search_google_scholar_papers`   | Search academic papers across disciplines with citation data   | APaper          |
| **Web Search**           | `qwen_search_web_search`                | Search the web using Qwen/Dashscope API                        | Qwen Search      |
| **GitHub Repository**     | `github-repo-mcp_getRepoAllDirectories` | Get all directories from a GitHub repository                   | GitHub-Repo-MCP |
|                           | `github-repo-mcp_getRepoDirectories`    | Get directories from a specific path in GitHub repository      | GitHub-Repo-MCP |
|                           | `github-repo-mcp_getRepoFile`           | Get file content from GitHub repository                        | GitHub-Repo-MCP |

All tools are implemented using FastMCP decorators with automatic registration, built-in validation, and enhanced error handling.

## Quick Start

- [**Video for Env Setup**](https://www.bilibili.com/video/BV1cZKozaEjg) [**Video for Claude code**](https://www.bilibili.com/video/BV1s9KmzVEcE/)
- [_Overview PDF_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/config.pdf) [_PDF for Claude code_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/config-claude.pdf)

### Prerequisites

- Python 3.10 or higher
- `pipx` for Python package installation
- `npx` for MCP Inspector (Node.js required)

### Integration with MCP Clients

Add the servers to your MCP client configuration:

#### VSCode Configuration (.vscode/mcp.json)

```json .vscode/mcp.json
{
  "servers": {
    "all-in-mcp": {
      "type": "stdio",
      "command": "pipx",
      "args": ["run", "all-in-mcp"],
      "env": {
        "APAPER": "true",
        "QWEN_SEARCH": "true",
        "DASHSCOPE_API_KEY": "your_api_key_here",
        "GITHUB_REPO_MCP": "true"
      }
    }
  }
}
```

#### Claude Code Configuration (.mcp.json)

```json .mcp.json
{
  "mcpServers": {
    "all-in-mcp": {
      "type": "stdio",
      "command": "pipx",
      "args": ["run", "all-in-mcp"],
      "env": {
        "APAPER": "true",
        "QWEN_SEARCH": "true",
        "DASHSCOPE_API_KEY": "your_api_key_here",
        "GITHUB_REPO_MCP": "true"
      }
    }
  }
}
```

### Server Options

The main proxy server supports multiple MCP backends through environment variables:

```bash
# Run with APaper academic tools enabled
APAPER=true pipx run all-in-mcp

# Run with Qwen Search web search enabled
QWEN_SEARCH=true DASHSCOPE_API_KEY=your_api_key_here pipx run all-in-mcp

# Run with GitHub repository tools enabled
GITHUB_REPO_MCP=true pipx run all-in-mcp

# Run with all backends enabled
APAPER=true QWEN_SEARCH=true DASHSCOPE_API_KEY=your_api_key_here GITHUB_REPO_MCP=true pipx run all-in-mcp

# Run standalone APaper server (academic tools only)
pipx run apaper

# Run standalone Qwen Search server (web search only)
DASHSCOPE_API_KEY=your_api_key_here pipx run qwen-search
```

> **Note**: If you have the package installed globally, you can also run directly: `all-in-mcp` or `qwen-search`

## Debugging & Testing

### MCP Inspector

Use the official MCP Inspector to debug and test server functionality:

```bash
# Debug the main proxy server with APaper tools
APAPER=true npx @modelcontextprotocol/inspector pipx run all-in-mcp

# Debug with all backends enabled
APAPER=true GITHUB_REPO_MCP=true npx @modelcontextprotocol/inspector pipx run all-in-mcp

# Debug standalone APaper server
npx @modelcontextprotocol/inspector pipx run apaper
```

#### Local Development with uv

When developing locally, use `uv run` to debug specific MCP functions:

```bash
# Debug APaper server (academic tools)
npx @modelcontextprotocol/inspector uv run apaper

# Debug all-in-mcp proxy with APaper enabled
APAPER=true npx @modelcontextprotocol/inspector uv run all-in-mcp

# Debug all-in-mcp proxy with GitHub repo tools enabled
GITHUB_REPO_MCP=true npx @modelcontextprotocol/inspector uv run all-in-mcp

# Debug all-in-mcp with all backends enabled
APAPER=true QWEN_SEARCH=true DASHSCOPE_API_KEY=your_api_key_here GITHUB_REPO_MCP=true npx @modelcontextprotocol/inspector uv run all-in-mcp

# Debug Qwen Search server
DASHSCOPE_API_KEY=your_api_key_here npx @modelcontextprotocol/inspector uv run qwen-search
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
uv run python tests/test_qwen_search.py
```

</details>
