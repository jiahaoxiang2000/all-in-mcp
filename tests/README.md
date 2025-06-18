# Tests

This directory contains tests for the all-in-mcp server.

## Running Tests

To run the tests, first install the development dependencies:

```bash
uv sync --extra dev
```

Then run the tests:

```bash
uv run pytest
```

Or run with more verbose output:

```bash
uv run pytest -v
```

## Test Structure

- `test_server.py` - Tests for the Base64 encoding functionality

## Test Coverage

The tests cover:
- Basic Base64 encoding functionality
- Edge cases (empty strings, special characters, Unicode)
- Error handling (unknown tools)
- Various input scenarios
