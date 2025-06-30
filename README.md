# All-in-MCP

An MCP (Model Context Protocol) server that provides utility functions, including academic paper search capabilities.

- [**Paper Tools overview _Video_**](https://www.bilibili.com/video/BV1RMKWzdEk8)
- [_Overview PDF_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/setup.pdf)

![APaper Research Direction](docs/APaper-research-direction-7x-2k-extended.gif)

## Features

This MCP server exposes the following daily-use utility tools as MCP endpoints:

### Available Tools

- **Academic Research**:
  - `search-iacr-papers`: Search academic papers from IACR ePrint Archive
  - `download-iacr-paper`: Download PDF of an IACR ePrint paper
  - `read-iacr-paper`: Read and extract text content from an IACR ePrint paper PDF
- **Bibliography Search**:
  - `search-cryptobib-papers`: Search CryptoBib bibliography database for cryptography papers (structured metadata or raw BibTeX)
- **Crossref Search**:
  - `search-crossref-papers`: Search academic papers from Crossref database
- **Google Scholar**:
  - `search-google-scholar-papers`: Search academic papers across disciplines with citation data
- **PDF Reading**:
  - `read-pdf`: Read and extract text from local and online PDF files

All tools are implemented as async MCP endpoints with proper validation and error handling.

## Quick Start

- [**Video for Env Setup**](https://www.bilibili.com/video/BV1cZKozaEjg) [**Video for Claude code**](https://www.bilibili.com/video/BV1s9KmzVEcE/)
- [_Overview PDF_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/config.pdf) [_PDF for Claude code_](https://github.com/jiahaoxiang2000/tutor/blob/main/Apaper/config-claude.pdf)

### Prerequisites

- Python 3.10 or higher
- UV package manager

### Installation

Install from PyPI (Recommended by `UV`)

```bash
uv pip install all-in-mcp
```

### Integration with MCP Clients

Add this server to your MCP client configuration. The server runs using stdio transport.

#### VSCode Configuration

```json .vscode/mcp.json
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

#### Claude Code Configuration

```json .mcp.json
{
  "mcpServers": {
    "all-in-mcp": {
      "command": "uv",
      "args": ["run", "all-in-mcp"]
    }
  }
}
```

<details>
<summary>Development</summary>

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
```

</details>
