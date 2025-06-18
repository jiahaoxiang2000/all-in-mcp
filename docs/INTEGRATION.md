# Example MCP Client Configurations

This file contains example configurations for integrating the all-in-mcp server with various MCP clients.

## Claude Desktop

Add this to your Claude Desktop `config.json`:

```json
{
  "mcpServers": {
    "all-in-mcp": {
      "command": "uv",
      "args": ["run", "all-in-mcp"],
      "cwd": "/path/to/your/all-in-mcp"
    }
  }
}
```

## Continue.dev

Add this to your Continue config:

```json
{
  "mcpServers": [
    {
      "name": "all-in-mcp",
      "command": ["uv", "run", "all-in-mcp"],
      "cwd": "/path/to/your/all-in-mcp"
    }
  ]
}
```

## VS Code MCP Extension

If using the VS Code MCP extension, add this to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "all-in-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "all-in-mcp"]
    }
  }
}
```

## Direct Usage

You can also run the server directly for testing:

```bash
# In the project directory
uv run all-in-mcp
```

The server will start and listen for MCP protocol messages on stdin/stdout.
