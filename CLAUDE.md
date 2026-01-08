# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

All-in-MCP is a FastMCP-based Model Context Protocol (MCP) proxy server that provides academic paper search and PDF processing utilities. The project has been restructured into two main components:

1. **APaper**: An isolated academic research module with tools for searching papers from multiple academic platforms
2. **All-in-MCP Proxy**: A FastMCP proxy server that forwards requests to APaper and other MCP servers

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

### All-in-MCP Proxy Structure

```
src/all_in_mcp/
├── __init__.py             # Package entry point
└── server.py              # FastMCP proxy server that imports APaper tools
```

### FastMCP Server Implementation

- **APaper Server**: `src/apaper/server.py` - Dedicated academic research server using FastMCP decorators
- **Proxy Server**: `src/all_in_mcp/server.py` - Main proxy server that imports and exposes APaper functionality
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

# Test server imports
uv run python -c "import all_in_mcp.server; print('Proxy server OK')"
uv run python -c "import apaper.server; print('APaper server OK')"
```

### Building and Distribution

```bash
# Build package (includes both all-in-mcp and apaper)
uv build
make build

# Clean build artifacts
make clean
```

## Testing Strategy

- **Unit Tests**: Located in `tests/` directory
- **New Test Structure**:
  - `test_apaper_*`: Tests for APaper module functionality
  - `test_fastmcp_server.py`: Tests for FastMCP server functionality
- **Test Execution**: Use `uv run python` for individual test files

## Key Implementation Details

### FastMCP Benefits

- **Simplified Development**: Automatic tool registration using decorators
- **Better Error Handling**: Built-in error management and logging
- **Enhanced Performance**: Optimized request handling and caching
- **Modern Architecture**: Clean separation between academic functionality and proxy server

## important-instruction-reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (\*.md) or README files. Only create documentation files if explicitly requested by the User.
