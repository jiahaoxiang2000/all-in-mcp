# all_in_mcp/server.py
"""
All-in-MCP FastMCP Proxy Server

This server uses ProxyClient to automatically proxy requests to the APaper server
and other MCP servers with advanced features like LLM sampling forwarding,
progress reporting, and logging.

Environment variables to enable MCP servers (all disabled by default):
- ENABLE_APAPER=true: Enable APaper academic search server
- ENABLE_GITHUB_REPO_MCP=true: Enable GitHub repository MCP server
"""

import os
from pathlib import Path
from fastmcp import FastMCP


def _str_to_bool(value: str) -> bool:
    """Convert string environment variable to boolean."""
    return value.lower() in ("true", "1", "yes", "on")


# Get the path to the APaper server
current_dir = Path(__file__).parent
apaper_server_path = current_dir.parent / "apaper" / "server.py"

# Build configuration based on environment variables
# All MCP servers are disabled by default
config = {"mcpServers": {}}

# APaper server (academic research tools)
if _str_to_bool(os.getenv("APAPER", "false")):
    config["mcpServers"]["apaper"] = {
        "type": "stdio",
        "command": "python",
        "args": [str(apaper_server_path)],
    }

# GitHub repository MCP server
if _str_to_bool(os.getenv("GITHUB_REPO_MCP", "false")):
    config["mcpServers"]["github-repo-mcp"] = {
        "type": "stdio",
        "command": "npx",
        "args": ["github-repo-mcp"],
    }

# Create proxy server from config (supports multiple backends)
app = FastMCP.as_proxy(config, name="All-in-MCP Proxy")


def main():
    """Main entry point for the all-in-mcp proxy server."""
    app.run()


if __name__ == "__main__":
    main()
