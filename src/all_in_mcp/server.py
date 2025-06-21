import os
from typing import List, Dict
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Import IACR searcher
from .academic_platforms.iacr import IACRSearcher

server = Server("all-in-mcp")

# Initialize IACR searcher
iacr_searcher = IACRSearcher()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available daily utility tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="search-iacr-papers",
            description="Search academic papers from IACR ePrint Archive",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string (e.g., 'cryptography', 'secret sharing')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of papers to return (default: 10)",
                        "default": 10,
                    },
                    "fetch_details": {
                        "type": "boolean",
                        "description": "Whether to fetch detailed information for each paper (default: True)",
                        "default": True,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="download-iacr-paper",
            description="Download PDF of an IACR ePrint paper",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "IACR paper ID (e.g., '2009/101')",
                    },
                    "save_path": {
                        "type": "string",
                        "description": "Directory to save the PDF (default: './downloads')",
                        "default": "./downloads",
                    },
                },
                "required": ["paper_id"],
            },
        ),
        types.Tool(
            name="read-iacr-paper",
            description="Read and extract text content from an IACR ePrint paper PDF",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "IACR paper ID (e.g., '2009/101')",
                    },
                    "save_path": {
                        "type": "string",
                        "description": "Directory where the PDF is/will be saved (default: './downloads')",
                        "default": "./downloads",
                    },
                },
                "required": ["paper_id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if not arguments:
        arguments = {}

    try:
        if name == "search-iacr-papers":
            query = arguments.get("query", "")
            max_results = arguments.get("max_results", 10)
            fetch_details = arguments.get("fetch_details", True)

            if not query:
                return [
                    types.TextContent(
                        type="text", text="Error: Query parameter is required"
                    )
                ]

            papers = iacr_searcher.search(query, max_results, fetch_details)

            if not papers:
                return [
                    types.TextContent(
                        type="text", text=f"No papers found for query: {query}"
                    )
                ]

            # Format the results
            result_text = f"Found {len(papers)} IACR papers for query '{query}':\n\n"
            for i, paper in enumerate(papers, 1):
                result_text += f"{i}. **{paper.title}**\n"
                result_text += f"   - Paper ID: {paper.paper_id}\n"
                result_text += f"   - Authors: {', '.join(paper.authors)}\n"
                result_text += f"   - URL: {paper.url}\n"
                result_text += f"   - PDF: {paper.pdf_url}\n"
                if paper.categories:
                    result_text += f"   - Categories: {', '.join(paper.categories)}\n"
                if paper.keywords:
                    result_text += f"   - Keywords: {', '.join(paper.keywords)}\n"
                if paper.abstract:
                    result_text += f"   - Abstract: {paper.abstract}n"
                result_text += "\n"

            return [types.TextContent(type="text", text=result_text)]

        elif name == "download-iacr-paper":
            paper_id = arguments.get("paper_id", "")
            save_path = arguments.get("save_path", "./downloads")

            if not paper_id:
                return [
                    types.TextContent(
                        type="text", text="Error: paper_id parameter is required"
                    )
                ]

            result = iacr_searcher.download_pdf(paper_id, save_path)

            if result.startswith(("Error", "Failed")):
                return [
                    types.TextContent(type="text", text=f"Download failed: {result}")
                ]
            else:
                return [
                    types.TextContent(
                        type="text", text=f"PDF downloaded successfully to: {result}"
                    )
                ]

        elif name == "read-iacr-paper":
            paper_id = arguments.get("paper_id", "")
            save_path = arguments.get("save_path", "./downloads")

            if not paper_id:
                return [
                    types.TextContent(
                        type="text", text="Error: paper_id parameter is required"
                    )
                ]

            result = iacr_searcher.read_paper(paper_id, save_path)

            if result.startswith("Error"):
                return [types.TextContent(type="text", text=result)]
            else:
                # Truncate very long text for display
                if len(result) > 5000:
                    truncated_result = (
                        result[:5000]
                        + f"\n\n... [Text truncated. Full text is {len(result)} characters long]"
                    )
                    return [types.TextContent(type="text", text=truncated_result)]
                else:
                    return [types.TextContent(type="text", text=result)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing {name}: {e!s}")]


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="all-in-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
