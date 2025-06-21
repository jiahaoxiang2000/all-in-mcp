# All-in-MCP

An MCP (Model Context Protocol) server that provides daily-use utility functions, including academic paper search capabilities.

## Features

### Daily Utilities

- **Academic Research**: IACR ePrint Archive paper search, download, and reading
- **Bibliography Search**: CryptoBib database search for cryptography papers

### Paper Search Capabilities

#### IACR ePrint Archive

- Search academic papers from IACR ePrint Archive
- Download PDF files
- Extract and read text content from papers
- Metadata extraction (authors, publication dates, abstracts)

#### CryptoBib Database

- Search comprehensive cryptography bibliography database
- Access to thousands of cryptographic research papers
- Retrieve structured paper metadata or raw BibTeX entries
- Support for all major cryptography venues and conferences

## Quick Start

### Prerequisites

- Python 3.12 or higher
- UV package manager

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install all-in-mcp
```

### Option 2: Install from Source

1. Clone this repository:

   ```bash
   git clone https://github.com/jiahaoxiang2000/all-in-mcp.git
   cd all-in-mcp
   ```

2. Install with UV:

   ```bash
   uv sync
   ```

### Running the Server

After installation, you can run the MCP server directly:

```bash
all-in-mcp
```

Or if you installed from source with UV:

```bash
uv run all-in-mcp
```

## Integration with MCP Clients

Add this server to your MCP client configuration. The server runs using stdio transport.
See detailed integration guide in [`docs/INTEGRATION.md`](docs/INTEGRATION.md).

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

## Development

For development setup and contribution guidelines, see the [Development Guide](docs/development.md).

### Quick Development Setup

```bash
# Clone the repository
git clone https://github.com/jiahaoxiang2000/all-in-mcp.git
cd all-in-mcp

# Install with development dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Run linting
uv run ruff check src/
uv run ruff format src/

# Type checking
uv run mypy src/all_in_mcp
```

### Releases

This project uses the existing release helper script for creating releases:

#### Using the Release Script

Use the release helper script to create a new version:

```bash
python scripts/release.py 0.1.2
```

This script will:

1. Update the version in `pyproject.toml`
2. Create a git commit
3. Create a git tag
4. Push the changes to trigger CI/CD

#### Manual Process

Alternatively, you can manually:

1. **Update version** in `pyproject.toml`:

   ```toml
   version = "0.1.2"  # Change this
   ```

2. **Commit and tag**:

   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.2"
   git tag v0.1.2
   git push --follow-tags
   ```

### Debugging

For debugging, use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/all-in-mcp run all-in-mcp
```

## Documentation

Complete documentation is available in the [`docs/`](docs/) directory:

- **[API Reference](docs/api.md)** - Complete API documentation
- **[Installation Guide](docs/installation.md)** - Setup instructions
- **[IACR Integration](docs/iacr.md)** - Academic paper search details
- **[CryptoBib Integration](docs/cryptobib.md)** - Bibliography database search
- **[Development Guide](docs/development.md)** - Contributing guidelines
- **[PyPI Setup Guide](docs/pypi-setup.md)** - Publishing configuration
- **[Examples](docs/examples.md)** - Usage examples
