# qwen_search/server.py
"""FastMCP-based web search server using Qwen/Dashscope API."""

import sys
from pathlib import Path

# Add the parent directory to path for absolute imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from fastmcp import FastMCP
from qwen_search.client import QwenSearchClient, QwenSearchError

# Initialize FastMCP server
mcp = FastMCP("qwen_search")

# Initialize the client (will read DASHSCOPE_API_KEY from environment)
# We don't initialize it here to avoid errors if the key is not set


@mcp.tool()
async def web_search(query: str, max_results: int = 10) -> str:
    """
    Search the web using Qwen/Dashscope API

    Args:
        query: Search query string (e.g., 'machine learning', 'climate change')
        max_results: Maximum number of results to return (default: 10)
    """
    try:
        # Initialize client (will check for API key)
        client = QwenSearchClient()

        # Make async call directly (FastMCP handles the event loop)
        result = await client.search(query, max_results)
        return result

    except QwenSearchError as e:
        return f"Search error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def main():
    """Main entry point for the Qwen Search MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
