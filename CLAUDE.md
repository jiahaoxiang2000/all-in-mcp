# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

All-in-MCP is a FastMCP-based Model Context Protocol (MCP) proxy server that provides academic paper search, web search, and PDF processing utilities. The project has been restructured into three main components:

1. **APaper**: An isolated academic research module with tools for searching papers from multiple academic platforms
2. **Qwen Search**: A web search module using the Qwen/Dashscope API
3. **All-in-MCP Proxy**: A FastMCP proxy server that forwards requests to APaper, Qwen Search, and other MCP servers

The system uses the FastMCP framework for simplified MCP server development with automatic tool registration, enhanced features, and better performance.

## New Architecture (FastMCP-based)

### APaper Module Structure

```
src/apaper/
├── __init__.py              # APaper package entry point
├── server.py               # FastMCP-based APaper server
├── models/
│   ├── __init__.py
│   └── paper.py           # Standardized Paper dataclass
├── platforms/             # Academic platform implementations
│   ├── __init__.py
│   ├── base.py           # Abstract PaperSource class
│   ├── iacr.py          # IACR ePrint Archive integration
│   ├── dblp.py          # DBLP computer science bibliography
│   └── google_scholar.py # Google Scholar search
```

### Qwen Search Module Structure

```
src/qwen_search/
├── __init__.py              # Qwen Search package entry point
└── server.py               # FastMCP-based Qwen Search proxy server
```

### All-in-MCP Proxy Structure

```
src/all_in_mcp/
├── __init__.py             # Package entry point
└── server.py              # FastMCP proxy server that imports APaper tools
```

### FastMCP Server Implementation

- **APaper Server**: `src/apaper/server.py` - Dedicated academic research server using FastMCP decorators
- **Qwen Search Server**: `src/qwen_search/server.py` - Proxy server that uses MCP SDK to connect to Dashscope SSE-based MCP server
- **Proxy Server**: `src/all_in_mcp/server.py` - Main proxy server that connects to APaper (stdio), Qwen Search (SSE), and other MCP servers
- **Tool Registration**: Uses FastMCP `@app.tool()` decorators for automatic tool registration
- **Data Model**: `src/apaper/models/paper.py` - Standardized `Paper` dataclass

### Available Academic Platforms

- **IACR**: `apaper/platforms/iacr.py` - IACR ePrint Archive integration
- **DBLP**: `apaper/platforms/dblp.py` - DBLP computer science bibliography with BibTeX export
- **Google Scholar**: `apaper/platforms/google_scholar.py` - Google Scholar search

## Development Commands

### Environment Setup

```bash
# Install development dependencies
uv sync --extra dev

# Install all dependencies (includes system dependencies)
make install-all
```

### Testing

```bash
# Run all tests
uv run python tests/test_fastmcp_server.py

# Run APaper-specific tests
uv run python tests/test_apaper_iacr.py
uv run python tests/test_apaper_pdf.py

# Run Qwen Search tests
uv run python tests/test_qwen_search.py

# Using make commands (if available)
make test
make test-verbose
```

### Running the Servers

```bash
# Run the main all-in-mcp proxy server
uv run all-in-mcp

# Run the isolated APaper server directly
uv run apaper

# Run the isolated Qwen Search server directly
uv run qwen-search

# Test server imports
uv run python -c "import all_in_mcp.server; print('Proxy server OK')"
uv run python -c "import apaper.server; print('APaper server OK')"
uv run python -c "import qwen_search.server; print('Qwen Search server OK')"
```

### Building and Distribution

```bash
# Build package (includes both all-in-mcp and apaper)
uv build
make build

# Clean build artifacts
make clean
```

## Environment Variables

To enable/disable MCP servers in the all-in-mcp proxy server, set the following environment variables:

- `APAPER=true` (default: false): Enable APaper academic search server
- `QWEN_SEARCH=true` (default: false): Enable Qwen/Dashscope web search server
- `GITHUB_REPO_MCP=true` (default: false): Enable GitHub repository MCP server

Additionally, the Qwen Search module requires:

- `DASHSCOPE_API_KEY`: Your Dashscope API key for accessing the Qwen Search API

## Testing Strategy

- **Unit Tests**: Located in `tests/` directory
- **New Test Structure**:
  - `test_apaper_*`: Tests for APaper module functionality
  - `test_qwen_search.py`: Tests for Qwen Search module functionality
  - `test_fastmcp_server.py`: Tests for FastMCP server functionality
- **Test Execution**: Use `uv run python` for individual test files

## Key Implementation Details

### FastMCP Benefits

- **Simplified Development**: Automatic tool registration using decorators
- **Better Error Handling**: Built-in error management and logging
- **Enhanced Performance**: Optimized request handling and caching
- **Modern Architecture**: Clean separation between academic functionality and proxy server

### SSE-based MCP Integration

The Qwen Search module demonstrates FastMCP's ability to connect to external SSE-based MCP servers:

- **Dashscope Integration**: Direct SSE connection to Dashscope's WebSearch MCP server
- **MCP SDK**: Uses FastMCP's built-in SSE transport to handle the connection
- **No Custom Parsing**: Leverages MCP SDK's robust SSE parsing instead of manual implementation
- **Seamless Tool Forwarding**: Automatically exposes Dashscope's search tools through the proxy

To use Qwen Search:
1. Set `QWEN_SEARCH=true` to enable the server
2. Set `DASHSCOPE_API_KEY` with your Dashscope API key
3. The proxy server automatically connects to Dashscope's SSE endpoint and forwards search requests

## important-instruction-reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (\*.md) or README files. Only create documentation files if explicitly requested by the User.
