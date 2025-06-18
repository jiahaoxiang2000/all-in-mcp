# Configuration Guide

This guide covers configuration options and customization for the All-in-MCP server.

## Server Configuration

### Basic Configuration

The server can be configured through environment variables or configuration files.

### Environment Variables

```bash
# Server settings
MCP_SERVER_NAME="all-in-mcp"
MCP_SERVER_VERSION="0.1.0"

# Download settings
DEFAULT_DOWNLOAD_DIR="./downloads"
MAX_DOWNLOAD_SIZE="100MB"

# Academic platform settings
IACR_BASE_URL="https://eprint.iacr.org"
IACR_MAX_RETRIES=3
IACR_TIMEOUT=30

# Logging
LOG_LEVEL="INFO"
LOG_FILE="all-in-mcp.log"
```

### Configuration File

Create a `config.toml` file in the project root:

```toml
[server]
name = "all-in-mcp"
version = "0.1.0"
debug = false

[downloads]
default_dir = "./downloads"
max_size = "100MB"
auto_cleanup = false

[iacr]
base_url = "https://eprint.iacr.org"
max_retries = 3
timeout = 30
user_agent = "All-in-MCP Academic Search"

[logging]
level = "INFO"
file = "all-in-mcp.log"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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

### Other MCP Clients

For other MCP clients, use the standard MCP connection:

```python
import mcp.client.stdio

# Connect to the server
async with mcp.client.stdio.stdio_client(
    command="uv",
    args=["run", "--directory", "/path/to/all-in-mcp", "all-in-mcp"]
) as client:
    # Use the client
    tools = await client.list_tools()
```

## Academic Platform Configuration

### IACR ePrint Archive

```python
IACR_CONFIG = {
    "base_url": "https://eprint.iacr.org",
    "search_endpoint": "/search",
    "pdf_endpoint": "/{paper_id}.pdf",
    "max_retries": 3,
    "timeout": 30,
    "rate_limit_delay": 1.0,
    "user_agent": "All-in-MCP Academic Search"
}
```

### Adding New Platforms

To configure new academic platforms:

1. **Create platform config**:

```python
PLATFORM_CONFIG = {
    "base_url": "https://platform.example.com",
    "api_key": os.getenv("PLATFORM_API_KEY"),
    "rate_limit": 10,  # requests per second
    "timeout": 30
}
```

2. **Register in settings**:

```python
ACADEMIC_PLATFORMS = {
    "iacr": IACR_CONFIG,
    "your_platform": PLATFORM_CONFIG
}
```

## Security Configuration

### API Keys

Store sensitive information in environment variables:

```bash
# Academic platform API keys
ARXIV_API_KEY="your_arxiv_key"
PUBMED_API_KEY="your_pubmed_key"

# Optional authentication
MCP_AUTH_TOKEN="your_auth_token"
```

### File System Security

```python
SECURITY_CONFIG = {
    "allowed_download_dirs": [
        "./downloads",
        "/tmp/papers",
        "/user/documents/papers"
    ],
    "max_file_size": "100MB",
    "allowed_extensions": [".pdf", ".txt"],
    "scan_downloads": True
}
```

## Performance Configuration

### Caching

```python
CACHE_CONFIG = {
    "enabled": True,
    "backend": "memory",  # or "redis", "file"
    "ttl": 3600,  # 1 hour
    "max_size": "100MB"
}
```

### Connection Pooling

```python
HTTP_CONFIG = {
    "max_connections": 100,
    "max_keepalive_connections": 20,
    "keepalive_expiry": 30,
    "timeout": 30
}
```

### Rate Limiting

```python
RATE_LIMIT_CONFIG = {
    "enabled": True,
    "requests_per_minute": 60,
    "burst_size": 10,
    "per_client": True
}
```

## Logging Configuration

### Log Levels

- `DEBUG`: Detailed information for diagnosing problems
- `INFO`: General information about server operation
- `WARNING`: Something unexpected happened
- `ERROR`: Serious problem occurred
- `CRITICAL`: Very serious error occurred

### Log Format

```python
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "all-in-mcp.log",
            "formatter": "detailed"
        }
    },
    "loggers": {
        "all_in_mcp": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}
```

## Development Configuration

### Debug Mode

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### Test Configuration

```python
TEST_CONFIG = {
    "mock_external_apis": True,
    "test_data_dir": "./test_data",
    "temp_download_dir": "/tmp/test_downloads",
    "cleanup_after_tests": True
}
```

## Deployment Configuration

### Production Settings

```bash
# Production environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
ENABLE_AUTH=true
AUTH_TOKEN_REQUIRED=true

# Performance
ENABLE_CACHING=true
RATE_LIMITING=true
MAX_CONCURRENT_REQUESTS=50
```

### Docker Configuration

```dockerfile
# Environment variables for Docker
ENV MCP_SERVER_NAME=all-in-mcp
ENV DEFAULT_DOWNLOAD_DIR=/app/downloads
ENV LOG_LEVEL=INFO
ENV DEBUG=false
```

## Troubleshooting Configuration

### Common Configuration Issues

**Permission Errors**:

- Check download directory permissions
- Verify user has write access
- Check file system quota

**Network Issues**:

- Verify proxy settings
- Check firewall rules
- Test DNS resolution

**Performance Issues**:

- Adjust timeout values
- Modify rate limiting
- Check resource limits

### Configuration Validation

```python
def validate_config():
    """Validate configuration settings."""
    errors = []

    # Check required settings
    if not os.path.exists(config.download_dir):
        errors.append(f"Download directory does not exist: {config.download_dir}")

    # Check network settings
    if config.timeout <= 0:
        errors.append("Timeout must be positive")

    if errors:
        raise ConfigurationError("\n".join(errors))
```
