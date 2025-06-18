# Examples

This directory contains example scripts demonstrating the functionality of the all-in-mcp server.

## Files

### `test_iacr_search.py`

A standalone example that demonstrates the IACR paper search functionality:

- Search for papers by keywords
- Download PDF files
- Extract text content from papers

Run with:

```bash
cd examples
python test_iacr_search.py
```

### `mcp_demo.py`

A comprehensive demo of the MCP server functionality:

- Lists all available tools
- Tests Base64 encoding
- Tests IACR paper search, download, and reading

Run with:

```bash
cd examples
python mcp_demo.py
```

## Requirements

Make sure you have installed the dependencies:

```bash
uv sync
```

## Note

These examples are for demonstration purposes. Some operations (like downloading and reading papers) may take time depending on network speed and paper size.
