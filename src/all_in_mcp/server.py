# all_in_mcp/server.py
"""
All-in-MCP FastMCP Proxy Server

This server uses ProxyClient to automatically proxy requests to the APaper server
with advanced features like LLM sampling forwarding, progress reporting, and logging.
"""

from pathlib import Path
from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

# Get the path to the APaper server
current_dir = Path(__file__).parent
apaper_server_path = current_dir.parent / "apaper" / "server.py"

# Initialize ProxyClient for APaper backend
backend = ProxyClient(str(apaper_server_path))

# Create proxy server that forwards all requests to APaper
app = FastMCP.as_proxy(backend)


def main():
    """Main entry point for the all-in-mcp proxy server."""
    app.run()


if __name__ == "__main__":
    main()
