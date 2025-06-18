# Tests

This directory contains unit tests for the all-in-mcp server functionality.

## Files

### `test_iacr.py`

Unit tests for the IACR paper search functionality:

- Basic search functionality
- Search parameter validation
- PDF download testing
- Paper reading functionality

### `test_mcp_server.py`

Unit tests for the MCP server:

- Tool listing functionality
- Base64 encoding tool
- IACR search tool integration
- Error handling

### `test_server.py` (existing)

Original server tests.

## Running Tests

Run all tests:

```bash
cd tests
python -m unittest discover
```

Run specific test file:

```bash
cd tests
python test_iacr.py
python test_mcp_server.py
```

## Requirements

Make sure you have installed the dependencies:

```bash
uv sync
```

## Test Coverage

The tests cover:

- Core MCP server functionality
- IACR paper search integration
- Error handling and edge cases
- Tool parameter validation
