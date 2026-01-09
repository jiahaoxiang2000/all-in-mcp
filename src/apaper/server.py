# apaper/server.py
"""FastMCP-based academic paper research server."""

import sys
from pathlib import Path

# Add the parent directory to path for absolute imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from fastmcp import FastMCP
from apaper.platforms import (
    IACRSearcher,
    DBLPSearcher,
    GoogleScholarSearcher,
)

# Initialize FastMCP server
mcp = FastMCP("apaper")

# Initialize searchers
iacr_searcher = IACRSearcher()
dblp_searcher = DBLPSearcher()
google_scholar_searcher = GoogleScholarSearcher()


@mcp.tool()
def search_iacr_papers(
    query: str,
    max_results: int = 10,
    fetch_details: bool = True,
    year_min: int | str | None = None,
    year_max: int | str | None = None,
) -> str:
    """
    Search academic papers from IACR ePrint Archive

    Args:
        query: Search query string (e.g., 'cryptography', 'secret sharing')
        max_results: Maximum number of papers to return (default: 10)
        fetch_details: Whether to fetch detailed information for each paper (default: True)
        year_min: Minimum publication year (revised after)
        year_max: Maximum publication year (revised before)
    """
    try:
        # Convert string parameters to integers if needed
        year_min_int = None
        year_max_int = None

        if year_min is not None:
            year_min_int = int(year_min)

        if year_max is not None:
            year_max_int = int(year_max)

        papers = iacr_searcher.search(
            query,
            max_results=max_results,
            fetch_details=fetch_details,
            year_min=year_min_int,
            year_max=year_max_int,
        )

        if not papers:
            year_filter_msg = ""
            if year_min or year_max:
                year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                year_filter_msg = f" in year range{year_range}"
            return f"No papers found for query: {query}{year_filter_msg}"

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
                result_text += f"   - Abstract: {paper.abstract}\n"
            result_text += "\n"

        return result_text
    except ValueError as e:
        return f"Error: Invalid year format. Please provide valid integers for year_min and year_max."
    except Exception as e:
        return f"Error searching IACR papers: {str(e)}"


@mcp.tool()
def download_iacr_paper(paper_id: str, save_path: str = "./downloads") -> str:
    """
    Download PDF of an IACR ePrint paper

    Args:
        paper_id: IACR paper ID (e.g., '2009/101')
        save_path: Directory to save the PDF (default: './downloads')
    """
    try:
        result = iacr_searcher.download_pdf(paper_id, save_path)

        if result.startswith(("Error", "Failed")):
            return f"Download failed: {result}"
        else:
            return f"PDF downloaded successfully to: {result}"
    except Exception as e:
        return f"Error downloading IACR paper: {str(e)}"


@mcp.tool()
def search_dblp_papers(
    query: str,
    max_results: int = 10,
    year_from: int | str | None = None,
    year_to: int | str | None = None,
    venue_filter: str | None = None,
    include_bibtex: bool = False,
) -> str:
    """
    Search DBLP computer science bibliography database for papers

    Args:
        query: Search query string (supports boolean 'and'/'or' operators)
        max_results: Maximum number of papers to return (default: 10)
        year_from: Lower bound for publication year (optional)
        year_to: Upper bound for publication year (optional)
        venue_filter: Case-insensitive substring filter for venues (e.g., 'ICLR', 'NeurIPS')
        include_bibtex: Whether to include BibTeX entries in results (default: False)
    """
    try:
        # Convert string parameters to integers if needed
        year_from_int = None
        year_to_int = None

        if year_from is not None:
            year_from_int = int(year_from)

        if year_to is not None:
            year_to_int = int(year_to)

        results = dblp_searcher.search(
            query,
            max_results=max_results,
            year_from=year_from_int,
            year_to=year_to_int,
            venue_filter=venue_filter,
            include_bibtex=include_bibtex,
        )

        if not results:
            filter_msg = ""
            filters = []
            if year_from or year_to:
                year_range = f"({year_from or 'earliest'}-{year_to or 'latest'})"
                filters.append(f"year range {year_range}")
            if venue_filter:
                filters.append(f"venue '{venue_filter}'")
            if filters:
                filter_msg = f" with filters: {', '.join(filters)}"
            return f"No papers found for query: {query}{filter_msg}"

        filter_msg = ""
        filters = []
        if year_from or year_to:
            year_range = f"({year_from or 'earliest'}-{year_to or 'latest'})"
            filters.append(f"year range {year_range}")
        if venue_filter:
            filters.append(f"venue '{venue_filter}'")
        if filters:
            filter_msg = f" with filters: {', '.join(filters)}"

        # If include_bibtex is True, results only contain BibTeX entries
        if include_bibtex:
            result_text = f"Found {len(results)} DBLP BibTeX entries for query '{query}'{filter_msg}:\n\n"
            for i, result in enumerate(results, 1):
                result_text += f"{i}. DBLP Key: {result.get('dblp_key', 'Unknown')}\n"
                result_text += f"```bibtex\n{result.get('bibtex', '')}\n```\n\n"
            return result_text

        # Otherwise, return full paper metadata
        result_text = (
            f"Found {len(results)} DBLP papers for query '{query}'{filter_msg}:\n\n"
        )
        for i, result in enumerate(results, 1):
            result_text += f"{i}. **{result.get('title', 'Untitled')}**\n"
            result_text += f"   - DBLP Key: {result.get('dblp_key', '')}\n"
            result_text += f"   - Authors: {', '.join(result.get('authors', []))}\n"
            if result.get("venue"):
                result_text += f"   - Venue: {result['venue']}\n"
            if result.get("year"):
                result_text += f"   - Year: {result['year']}\n"
            if result.get("doi"):
                result_text += f"   - DOI: {result['doi']}\n"
            if result.get("url"):
                result_text += f"   - URL: {result['url']}\n"
            result_text += "\n"

        return result_text
    except ValueError:
        return "Error: Invalid year format. Please provide valid integers for year_from and year_to."
    except Exception as e:
        return f"Error searching DBLP: {str(e)}"


@mcp.tool()
def search_google_scholar_papers(
    query: str,
    max_results: int = 10,
    year_low: int | str | None = None,
    year_high: int | str | None = None,
) -> str:
    """
    Search academic papers from Google Scholar

    Args:
        query: Search query string (e.g., 'machine learning', 'neural networks')
        max_results: Maximum number of papers to return (default: 10)
        year_low: Minimum publication year (optional)
        year_high: Maximum publication year (optional)
    """
    try:
        # Convert string parameters to integers if needed
        year_low_int = None
        year_high_int = None

        if year_low is not None:
            year_low_int = int(year_low)

        if year_high is not None:
            year_high_int = int(year_high)

        papers = google_scholar_searcher.search(
            query,
            max_results=max_results,
            year_low=year_low_int,
            year_high=year_high_int,
        )

        if not papers:
            year_filter_msg = ""
            if year_low or year_high:
                year_range = f" ({year_low or 'earliest'}-{year_high or 'latest'})"
                year_filter_msg = f" in year range{year_range}"
            return f"No papers found for query: {query}{year_filter_msg}"

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

        return result_text
    except ValueError as e:
        return f"Error: Invalid year format. Please provide valid integers for year_low and year_high."
    except Exception as e:
        return f"Error searching Google Scholar: {str(e)}"


def main():
    """Main entry point for the APaper MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
