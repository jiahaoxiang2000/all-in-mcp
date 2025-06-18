# Installation Guide

This guide covers the installation and setup of the All-in-MCP server.

## Requirements

- Python 3.12 or higher
- UV package manager (recommended) or pip
- Internet connection for downloading papers

## Installation Methods

### Method 1: Using UV (Recommended)

1. **Install UV** (if not already installed):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository**:

```bash
git clone <repository-url>
cd all-in-mcp
```

3. **Install dependencies**:

```bash
uv sync
```

4. **Run the server**:

```bash
uv run all-in-mcp
```

### Method 2: Using pip

1. **Clone the repository**:

```bash
git clone <repository-url>
cd all-in-mcp
```

2. **Create virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -e .
```

4. **Run the server**:

```bash
python -m all_in_mcp
```

## Verification

To verify the installation:

1. **Run tests**:

```bash
python -m unittest discover tests/
```

2. **Run examples**:

```bash
python examples/test_iacr_search.py
```

3. **Check available tools**:

```bash
python examples/mcp_demo.py
```

## Dependencies

The server requires these packages:

- `mcp>=1.9.4` - Model Context Protocol implementation
- `requests>=2.31.0` - HTTP requests
- `feedparser>=6.0.10` - RSS/Atom feed parsing
- `beautifulsoup4>=4.12.0` - HTML parsing
- `pypdf>=4.0.0` - PDF text extraction
- `httpx>=0.24.0` - Async HTTP client

## Troubleshooting

### Common Issues

**Import Errors**:

- Ensure all dependencies are installed
- Check Python version compatibility
- Verify virtual environment activation

**Network Issues**:

- Check internet connection
- Verify firewall settings
- Some academic sites may have rate limiting

**PDF Download Issues**:

- Ensure write permissions to download directory
- Check available disk space
- Some papers may not be available for download

### Getting Help

1. Check the error message carefully
2. Review the [Examples](examples.md) documentation
3. Run the test suite to identify issues
4. Check the GitHub issues for similar problems
