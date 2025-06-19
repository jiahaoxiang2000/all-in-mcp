# Configuration Guide

This guide covers configuration options for the All-in-MCP server.

## Environment Variables

```bash
# Download settings
DEFAULT_DOWNLOAD_DIR="./downloads"

# IACR settings
IACR_BASE_URL="https://eprint.iacr.org"
IACR_MAX_RETRIES=3
IACR_TIMEOUT=30

# Logging
LOG_LEVEL="INFO"
```

## MCP Client Integration

### Claude Desktop Integration

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "all-in-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/all-in-mcp", "all-in-mcp"],
      "env": {
        "LOG_LEVEL": "INFO",
        "DEFAULT_DOWNLOAD_DIR": "/path/to/downloads"
      }
    }
  }
}
```

## IACR Configuration

The IACR platform can be configured with these environment variables:

```bash
IACR_BASE_URL="https://eprint.iacr.org"
IACR_MAX_RETRIES=3
IACR_TIMEOUT=30
```

## Troubleshooting

### Common Configuration Issues

**Permission Errors**:

- Check download directory permissions
- Verify user has write access

**Network Issues**:

- Verify proxy settings
- Check firewall rules

**Performance Issues**:

- Adjust timeout values
- Check resource limits
