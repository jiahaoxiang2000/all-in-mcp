# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

All-in-MCP is a Model Context Protocol (MCP) server that provides academic paper search and PDF processing utilities. The server exposes tools for searching papers from multiple academic platforms (IACR, CryptoBib, Crossref, Google Scholar) and processing PDF documents.

## Core Architecture

### MCP Server Structure

- **Entry Point**: `src/all_in_mcp/server.py` - Main MCP server implementation
- **Tool Registration**: Tools are registered with JSON schemas in `handle_list_tools()`
- **Request Handling**: Tool calls are routed through `handle_call_tool()`
- **Data Model**: `src/all_in_mcp/paper.py` - Standardized `Paper` dataclass for all platforms

### Academic Platform Architecture

- **Base Class**: `src/all_in_mcp/academic_platforms/base.py` - Abstract `PaperSource` class
- **Platform Implementations**: Each academic platform inherits from `PaperSource` and implements:
  - `search(query, **kwargs) -> list[Paper]`
  - `download_pdf(paper_id, save_path) -> str`
  - `read_paper(paper_id, save_path) -> str`

### Available Platforms

- **IACR**: `academic_platforms/iacr.py` - IACR ePrint Archive integration
- **CryptoBib**: `academic_platforms/cryptobib.py` - Cryptography bibliography database
- **Crossref**: `academic_platforms/crossref.py` - Crossref academic database
- **Google Scholar**: `academic_platforms/google_scholar.py` - Google Scholar search

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
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_iacr.py

# Using make commands
make test
make test-verbose
```

### Running the Server

```bash
# Run MCP server
uv run all-in-mcp

# Run with debug output
make run-debug

# Test server import
make test-import
```

### Building and Distribution

```bash
# Build package
uv build
make build

# Clean build artifacts
make clean
```

## Adding New Academic Platforms

1. Create new platform class in `academic_platforms/` inheriting from `PaperSource`
2. Implement required methods: `search()`, `download_pdf()`, `read_paper()`
3. Add platform import and initialization in `server.py`
4. Register new tools in `handle_list_tools()` and `handle_call_tool()`
5. Add comprehensive tests in `tests/test_<platform>.py`

## Testing Strategy

- **Unit Tests**: Located in `tests/` directory, using pytest framework
- **Test Structure**: One test file per platform (e.g., `test_iacr.py`)
- **Async Support**: Tests support async operations with `asyncio_mode = "auto"`
- **Mocking**: Use `@patch` for external API calls during testing

## Configuration

- **Dependencies**: Managed in `pyproject.toml` with separate dev/system extras
- **Code Style**: Ruff formatting and linting configured in `pyproject.toml`
- **Type Checking**: MyPy configuration in `pyproject.toml`
- **Test Config**: Pytest configuration in `pytest.ini` and `pyproject.toml`

## Key Implementation Details

- All academic platforms return standardized `Paper` objects with consistent fields
- PDF processing uses `pypdf` library for text extraction
- HTTP requests use `httpx` for async support
- MCP server follows stdio transport protocol
- Error handling includes graceful degradation for network issues
