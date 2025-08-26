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
    CryptoBibSearcher,
    CrossrefSearcher,
    GoogleScholarSearcher
)
from apaper.utils.pdf_reader import read_pdf

# Initialize FastMCP server
mcp = FastMCP("apaper")

# Initialize searchers
iacr_searcher = IACRSearcher()
cryptobib_searcher = CryptoBibSearcher(cache_dir="./downloads")
crossref_searcher = CrossrefSearcher()
google_scholar_searcher = GoogleScholarSearcher()


@mcp.tool()
def search_iacr_papers(
    query: str,
    max_results: int = 10,
    fetch_details: bool = True,
    year_min: int | None = None,
    year_max: int | None = None,
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
            return f"No papers found for query: {query}{year_filter_msg}"

        # Format the results
        year_filter_msg = ""
        if year_min or year_max:
            year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
            year_filter_msg = f" in year range{year_range}"
        
        result_text = f"Found {len(papers)} IACR papers for query '{query}'{year_filter_msg}:\n\n"
        
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
def read_iacr_paper(
    paper_id: str,
    save_path: str = "./downloads",
    start_page: int | None = None,
    end_page: int | None = None,
) -> str:
    """
    Read and extract text content from an IACR ePrint paper PDF
    
    Args:
        paper_id: IACR paper ID (e.g., '2009/101')
        save_path: Directory where the PDF is/will be saved (default: './downloads')
        start_page: Starting page number (1-indexed, inclusive). Defaults to 1.
        end_page: Ending page number (1-indexed, inclusive). Defaults to last page.
    """
    try:
        result = iacr_searcher.read_paper(
            paper_id, save_path, start_page=start_page, end_page=end_page
        )

        if result.startswith("Error"):
            return result
        else:
            # Truncate very long text for display
            if len(result) > 5000:
                truncated_result = (
                    result[:5000]
                    + f"\n\n... [Text truncated. Full text is {len(result)} characters long]"
                )
                return truncated_result
            else:
                return result
    except Exception as e:
        return f"Error reading IACR paper: {str(e)}"


@mcp.tool()
def search_cryptobib_papers(
    query: str,
    max_results: int = 10,
    return_bibtex: bool = False,
    force_download: bool = False,
    year_min: int | None = None,
    year_max: int | None = None,
) -> str:
    """
    Search CryptoBib bibliography database for cryptography papers
    
    Args:
        query: Search query string (e.g., 'cryptography', 'lattice', 'homomorphic')
        max_results: Maximum number of papers to return (default: 10)
        return_bibtex: Whether to return raw BibTeX entries (default: False)
        force_download: Force download the newest crypto.bib file (default: False)
        year_min: Minimum publication year (inclusive, optional)
        year_max: Maximum publication year (inclusive, optional)
    """
    try:
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
                    year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                    year_filter_msg = f" in year range{year_range}"
                return f"No BibTeX entries found for query: {query}{year_filter_msg}"

            year_filter_msg = ""
            if year_min or year_max:
                year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                year_filter_msg = f" in year range{year_range}"
            
            result_text = f"Found {len(bibtex_entries)} BibTeX entries for query '{query}'{year_filter_msg}:\n\n"
            for i, entry in enumerate(bibtex_entries, 1):
                result_text += f"Entry {i}:\n```bibtex\n{entry}\n```\n\n"

            return result_text
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
                    year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                    year_filter_msg = f" in year range{year_range}"
                return f"No papers found for query: {query}{year_filter_msg}"

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
                result_text += "\n"

            return result_text
    except Exception as e:
        return f"Error searching CryptoBib papers: {str(e)}"


@mcp.tool()
def search_google_scholar_papers(
    query: str,
    max_results: int = 10,
    year_low: int | None = None,
    year_high: int | None = None,
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
        papers = google_scholar_searcher.search(
            query,
            max_results=max_results,
            year_low=year_low,
            year_high=year_high,
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
    except Exception as e:
        return f"Error searching Google Scholar: {str(e)}"


@mcp.tool()
def search_crossref_papers(
    query: str,
    max_results: int = 10,
    year_min: int | None = None,
    year_max: int | None = None,
    sort_by: str = "relevance",
) -> str:
    """
    Search academic papers from Crossref database
    
    Args:
        query: Search query string (e.g., 'quantum computing', 'machine learning')
        max_results: Maximum number of papers to return (default: 10)
        year_min: Minimum publication year (optional)
        year_max: Maximum publication year (optional)
        sort_by: Sort order: relevance, published, indexed, updated (default: relevance)
    """
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
                year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                year_filter_msg = f" in year range{year_range}"
            return f"No papers found for query: {query}{year_filter_msg}"

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

        return result_text
    except Exception as e:
        return f"Error searching Crossref: {str(e)}"


@mcp.tool()
def read_pdf_file(
    pdf_source: str,
    start_page: int | None = None,
    end_page: int | None = None,
) -> str:
    """
    Read and extract text content from a PDF file (local or online)
    
    Args:
        pdf_source: Path to local PDF file or URL to online PDF
        start_page: Starting page number (1-indexed, inclusive). Defaults to 1.
        end_page: Ending page number (1-indexed, inclusive). Defaults to last page.
    """
    try:
        result = read_pdf(pdf_source, start_page=start_page, end_page=end_page)
        return result
    except Exception as e:
        return f"Error reading PDF from {pdf_source}: {str(e)}"


def main():
    """Main entry point for the APaper MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()