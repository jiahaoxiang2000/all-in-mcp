import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from .academic_platforms.cryptobib import CryptoBibSearcher
from .academic_platforms.crossref import CrossrefSearcher
from .academic_platforms.google_scholar import GoogleScholarSearcher

# Import searchers
from .academic_platforms.iacr import IACRSearcher
from .paper import read_pdf

server = Server("all-in-mcp")

# Initialize searchers
iacr_searcher = IACRSearcher()
cryptobib_searcher = CryptoBibSearcher(cache_dir="./downloads")
crossref_searcher = CrossrefSearcher()
google_scholar_searcher = GoogleScholarSearcher()


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
                    "year_min": {
                        "type": "integer",
                        "description": "Minimum publication year (revised after)",
                    },
                    "year_max": {
                        "type": "integer",
                        "description": "Maximum publication year (revised before)",
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
                    "start_page": {
                        "type": "integer",
                        "description": "Starting page number (1-indexed, inclusive). Defaults to 1.",
                        "minimum": 1,
                    },
                    "end_page": {
                        "type": "integer",
                        "description": "Ending page number (1-indexed, inclusive). Defaults to last page.",
                        "minimum": 1,
                    },
                },
                "required": ["paper_id"],
            },
        ),
        types.Tool(
            name="search-cryptobib-papers",
            description="Search CryptoBib bibliography database for cryptography papers",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string (e.g., 'cryptography', 'lattice', 'homomorphic')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of papers to return (default: 10)",
                        "default": 10,
                    },
                    "return_bibtex": {
                        "type": "boolean",
                        "description": "Whether to return raw BibTeX entries (default: False)",
                        "default": False,
                    },
                    "force_download": {
                        "type": "boolean",
                        "description": "Force download the newest crypto.bib file (default: False)",
                        "default": False,
                    },
                    "year_min": {
                        "type": "integer",
                        "description": "Minimum publication year (inclusive, optional)",
                    },
                    "year_max": {
                        "type": "integer",
                        "description": "Maximum publication year (inclusive, optional)",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search-google-scholar-papers",
            description="Search academic papers from Google Scholar",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string (e.g., 'machine learning', 'neural networks')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of papers to return (default: 10)",
                        "default": 10,
                    },
                    "year_low": {
                        "type": "integer",
                        "description": "Minimum publication year (optional)",
                    },
                    "year_high": {
                        "type": "integer",
                        "description": "Maximum publication year (optional)",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search-crossref-papers",
            description="Search academic papers from Crossref database",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string (e.g., 'quantum computing', 'machine learning')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of papers to return (default: 10)",
                        "default": 10,
                    },
                    "year_min": {
                        "type": "integer",
                        "description": "Minimum publication year (optional)",
                    },
                    "year_max": {
                        "type": "integer",
                        "description": "Maximum publication year (optional)",
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "Sort order: relevance, published, indexed, updated (default: relevance)",
                        "default": "relevance",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="read-pdf",
            description="Read and extract text content from a PDF file (local or online)",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_source": {
                        "type": "string",
                        "description": "Path to local PDF file or URL to online PDF",
                    },
                    "start_page": {
                        "type": "integer",
                        "description": "Starting page number (1-indexed, inclusive). Defaults to 1.",
                        "minimum": 1,
                    },
                    "end_page": {
                        "type": "integer",
                        "description": "Ending page number (1-indexed, inclusive). Defaults to last page.",
                        "minimum": 1,
                    },
                },
                "required": ["pdf_source"],
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
            year_min = arguments.get("year_min")
            year_max = arguments.get("year_max")

            if not query:
                return [
                    types.TextContent(
                        type="text", text="Error: Query parameter is required"
                    )
                ]

            papers = iacr_searcher.search(
                query,
                max_results=max_results,
                fetch_details=fetch_details,
                year_min=year_min,
                year_max=year_max,
            )

            if not papers:
                year_filter_msg = ""
                if year_min or year_max:
                    year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                    year_filter_msg = f" in year range{year_range}"
                return [
                    types.TextContent(
                        type="text",
                        text=f"No papers found for query: {query}{year_filter_msg}",
                    )
                ]

            # Format the results
            year_filter_msg = ""
            if year_min or year_max:
                year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                year_filter_msg = f" in year range{year_range}"
            result_text = (
                f"Found {len(papers)} IACR papers for query '{query}'{year_filter_msg}:\n\n"
            )
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
            start_page = arguments.get("start_page")
            end_page = arguments.get("end_page")

            if not paper_id:
                return [
                    types.TextContent(
                        type="text", text="Error: paper_id parameter is required"
                    )
                ]

            result = iacr_searcher.read_paper(paper_id, save_path, start_page=start_page, end_page=end_page)

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

        elif name == "search-cryptobib-papers":
            query = arguments.get("query", "")
            max_results = arguments.get("max_results", 10)
            return_bibtex = arguments.get("return_bibtex", False)
            force_download = arguments.get("force_download", False)
            year_min = arguments.get("year_min")
            year_max = arguments.get("year_max")

            if not query:
                return [
                    types.TextContent(
                        type="text", text="Error: Query parameter is required"
                    )
                ]

            if return_bibtex:
                # Return raw BibTeX entries
                bibtex_entries = cryptobib_searcher.search_bibtex(
                    query,
                    max_results,
                    force_download=force_download,
                    year_min=year_min,
                    year_max=year_max,
                )

                if not bibtex_entries:
                    year_filter_msg = ""
                    if year_min or year_max:
                        year_range = (
                            f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                        )
                        year_filter_msg = f" in year range{year_range}"
                    return [
                        types.TextContent(
                            type="text",
                            text=f"No BibTeX entries found for query: {query}{year_filter_msg}",
                        )
                    ]

                year_filter_msg = ""
                if year_min or year_max:
                    year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                    year_filter_msg = f" in year range{year_range}"
                result_text = f"Found {len(bibtex_entries)} BibTeX entries for query '{query}'{year_filter_msg}:\n\n"
                for i, entry in enumerate(bibtex_entries, 1):
                    result_text += f"Entry {i}:\n```bibtex\n{entry}\n```\n\n"

                return [types.TextContent(type="text", text=result_text)]
            else:
                # Return parsed Paper objects
                papers = cryptobib_searcher.search(
                    query,
                    max_results,
                    force_download=force_download,
                    year_min=year_min,
                    year_max=year_max,
                )

                if not papers:
                    year_filter_msg = ""
                    if year_min or year_max:
                        year_range = (
                            f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                        )
                        year_filter_msg = f" in year range{year_range}"
                    return [
                        types.TextContent(
                            type="text",
                            text=f"No papers found for query: {query}{year_filter_msg}",
                        )
                    ]

                year_filter_msg = ""
                if year_min or year_max:
                    year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                    year_filter_msg = f" in year range{year_range}"
                result_text = f"Found {len(papers)} CryptoBib papers for query '{query}'{year_filter_msg}:\n\n"
                for i, paper in enumerate(papers, 1):
                    result_text += f"{i}. **{paper.title}**\n"
                    result_text += f"   - Entry Key: {paper.paper_id}\n"
                    result_text += f"   - Authors: {', '.join(paper.authors)}\n"
                    if paper.extra and "venue" in paper.extra:
                        result_text += f"   - Venue: {paper.extra['venue']}\n"
                    if paper.published_date and paper.published_date.year > 1900:
                        result_text += f"   - Year: {paper.published_date.year}\n"
                    if paper.doi:
                        result_text += f"   - DOI: {paper.doi}\n"
                    if paper.extra and "pages" in paper.extra:
                        result_text += f"   - Pages: {paper.extra['pages']}\n"
                    # Only include BibTeX when explicitly requested
                    if return_bibtex and paper.extra and "bibtex" in paper.extra:
                        result_text += (
                            f"   - BibTeX:\n```bibtex\n{paper.extra['bibtex']}\n```\n"
                        )
                    result_text += "\n"

                return [types.TextContent(type="text", text=result_text)]

        elif name == "search-google-scholar-papers":
            query = arguments.get("query", "")
            max_results = arguments.get("max_results", 10)
            year_low = arguments.get("year_low")
            year_high = arguments.get("year_high")

            if not query:
                return [
                    types.TextContent(
                        type="text", text="Error: Query parameter is required"
                    )
                ]

            try:
                papers = google_scholar_searcher.search(
                    query,
                    max_results=max_results,
                    year_low=year_low,
                    year_high=year_high,
                )

                if not papers:
                    year_filter_msg = ""
                    if year_low or year_high:
                        year_range = (
                            f" ({year_low or 'earliest'}-{year_high or 'latest'})"
                        )
                        year_filter_msg = f" in year range{year_range}"
                    return [
                        types.TextContent(
                            type="text",
                            text=f"No papers found for query: {query}{year_filter_msg}",
                        )
                    ]

                year_filter_msg = ""
                if year_low or year_high:
                    year_range = f" ({year_low or 'earliest'}-{year_high or 'latest'})"
                    year_filter_msg = f" in year range{year_range}"

                result_text = f"Found {len(papers)} Google Scholar papers for query '{query}'{year_filter_msg}:\n\n"
                for i, paper in enumerate(papers, 1):
                    result_text += f"{i}. **{paper.title}**\n"
                    result_text += f"   - Authors: {', '.join(paper.authors)}\n"
                    if paper.citations > 0:
                        result_text += f"   - Citations: {paper.citations}\n"
                    if paper.published_date and paper.published_date.year > 1900:
                        result_text += f"   - Year: {paper.published_date.year}\n"
                    if paper.url:
                        result_text += f"   - URL: {paper.url}\n"
                    if paper.abstract:
                        # Truncate abstract for readability
                        abstract_preview = (
                            paper.abstract[:300] + "..."
                            if len(paper.abstract) > 300
                            else paper.abstract
                        )
                        result_text += f"   - Abstract: {abstract_preview}\n"
                    result_text += "\n"

                return [types.TextContent(type="text", text=result_text)]

            except Exception as e:
                return [
                    types.TextContent(
                        type="text", text=f"Error searching Google Scholar: {e!s}"
                    )
                ]

        elif name == "search-crossref-papers":
            query = arguments.get("query", "")
            max_results = arguments.get("max_results", 10)
            year_min = arguments.get("year_min")
            year_max = arguments.get("year_max")
            sort_by = arguments.get("sort_by", "relevance")

            if not query:
                return [
                    types.TextContent(
                        type="text", text="Error: Query parameter is required"
                    )
                ]

            try:
                papers = crossref_searcher.search(
                    query,
                    max_results=max_results,
                    year_min=year_min,
                    year_max=year_max,
                    sort_by=sort_by,
                )

                if not papers:
                    year_filter_msg = ""
                    if year_min or year_max:
                        year_range = (
                            f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                        )
                        year_filter_msg = f" in year range{year_range}"
                    return [
                        types.TextContent(
                            type="text",
                            text=f"No papers found for query: {query}{year_filter_msg}",
                        )
                    ]

                year_filter_msg = ""
                if year_min or year_max:
                    year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                    year_filter_msg = f" in year range{year_range}"

                result_text = f"Found {len(papers)} Crossref papers for query '{query}'{year_filter_msg}:\n\n"
                for i, paper in enumerate(papers, 1):
                    result_text += f"{i}. **{paper.title}**\n"
                    result_text += f"   - Authors: {', '.join(paper.authors)}\n"
                    if paper.doi:
                        result_text += f"   - DOI: {paper.doi}\n"
                    if paper.citations > 0:
                        result_text += f"   - Citations: {paper.citations}\n"
                    if paper.published_date and paper.published_date.year > 1900:
                        result_text += f"   - Year: {paper.published_date.year}\n"
                    if paper.extra and paper.extra.get("journal"):
                        result_text += f"   - Journal: {paper.extra['journal']}\n"
                    if paper.extra and paper.extra.get("volume"):
                        result_text += f"   - Volume: {paper.extra['volume']}\n"
                    if paper.extra and paper.extra.get("pages"):
                        result_text += f"   - Pages: {paper.extra['pages']}\n"
                    if paper.url:
                        result_text += f"   - URL: {paper.url}\n"
                    if paper.abstract:
                        # Truncate abstract for readability
                        abstract_preview = (
                            paper.abstract[:300] + "..."
                            if len(paper.abstract) > 300
                            else paper.abstract
                        )
                        result_text += f"   - Abstract: {abstract_preview}\n"
                    result_text += "\n"

                return [types.TextContent(type="text", text=result_text)]

            except Exception as e:
                return [
                    types.TextContent(
                        type="text", text=f"Error searching Crossref: {e!s}"
                    )
                ]

        elif name == "read-pdf":
            pdf_source = arguments.get("pdf_source", "")
            start_page = arguments.get("start_page")
            end_page = arguments.get("end_page")

            if not pdf_source:
                return [
                    types.TextContent(
                        type="text", text="Error: pdf_source parameter is required"
                    )
                ]

            try:
                result = read_pdf(pdf_source, start_page=start_page, end_page=end_page)
                return [types.TextContent(type="text", text=result)]

            except Exception as e:
                return [
                    types.TextContent(
                        type="text", text=f"Error reading PDF from {pdf_source}: {e!s}"
                    )
                ]

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
