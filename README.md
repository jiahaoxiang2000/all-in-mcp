# all-in-mcp MCP server

MCP server providing daily-use utility functions for common tasks like text processing, encoding/decoding, hashing, and system information.

## Features

This MCP server provides the following daily utility tools:

## Installation

### Prerequisites

- Python 3.12 or higher
- UV package manager

### Setup

1. Clone or download this project
2. Install dependencies:

   ```bash
   uv sync
   ```

3. For optional system information features:
   ```bash
   uv sync --extra system
   ```

## Usage

### Running the Server

```bash
uv run all-in-mcp
```

### Integration with MCP Clients

Add this server to your MCP client configuration. The server runs using stdio transport.
Detail show on [integration](./INTEGRATION.md).

Example configuration for Claude Desktop:

```json
{
  "mcpServers": {
    "all-in-mcp": {
      "command": "uv",
      "args": ["run", "all-in-mcp"],
      "cwd": "/path/to/all-in-mcp"
    }
  }
}
```

## Tool Examples

### Text Encoding

- Encode text to Base64: `encode-base64` with `text` parameter
- Decode Base64: `decode-base64` with `encoded` parameter

### Hashing

- Generate SHA256 hash: `hash-text` with `text` and optional `algorithm` ("md5", "sha1", "sha256")

### URL Processing

- URL encode: `url-encode` with `text` parameter
- URL decode: `url-decode` with `encoded` parameter

### System Information

- Get basic info: `system-info` with default `details`
- Get specific info: `system-info` with `details` array (e.g., ["platform", "python", "memory"])

### Text Analysis

- Test regex: `regex-match` with `text`, `pattern`, and optional `flags`
- Count text metrics: `count-words` with `text` parameter

## Development

### Project Structure

- `src/all_in_mcp/server.py`: Main MCP server implementation
- `src/all_in_mcp/__init__.py`: Package initialization
- `pyproject.toml`: Project configuration and dependencies

### Adding New Tools

1. Add tool definition to `handle_list_tools()`
2. Implement tool logic in `handle_call_tool()`
3. Update README documentation

## Safety & Security

All tools are designed to be safe for daily use:

- No file system modifications
- No network requests
- Read-only system information access
- Input validation and error handling

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "all-in-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/home/isomo/py/all-in-mcp",
        "run",
        "all-in-mcp"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "all-in-mcp": {
      "command": "uvx",
      "args": [
        "all-in-mcp"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:

```bash
uv sync
```

2. Build package distributions:

```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:

```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:

- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /home/isomo/py/all-in-mcp run all-in-mcp
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
