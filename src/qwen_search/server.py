# qwen_search/server.py
"""FastMCP-based proxy server for Qwen/Dashscope Web Search MCP."""

import os
from pathlib import Path
import sys

# Add the parent directory to path for absolute imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from fastmcp import FastMCP


# Check if API key is available
api_key = os.getenv("DASHSCOPE_API_KEY")

if api_key:
    # Configure the Dashscope SSE MCP server
    config = {
        "mcpServers": {
            "qwen_search": {
                "type": "sse",
                "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse",
                "headers": {"Authorization": f"Bearer {api_key}"},
            }
        }
    }

    # Create proxy server that connects to the Dashscope SSE MCP server
    mcp = FastMCP.as_proxy(config, name="Qwen Search Proxy")
else:
    # If no API key, create a minimal server that will show an error
    mcp = FastMCP("Qwen Search Proxy")

    @mcp.tool()
    def web_search(query: str, max_results: int = 10) -> str:
        """
        Search the web using Qwen/Dashscope API

        Note: This tool requires DASHSCOPE_API_KEY environment variable to be set.

        Args:
            query: Search query string (e.g., 'machine learning', 'climate change')
            max_results: Maximum number of results to return (default: 10)
        """
        return "Error: DASHSCOPE_API_KEY not set. Please set the DASHSCOPE_API_KEY environment variable to use Qwen Search."


def main():
    """Main entry point for the Qwen Search MCP proxy server."""
    mcp.run()


if __name__ == "__main__":
    main()
