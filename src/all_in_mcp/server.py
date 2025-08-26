# all_in_mcp/server.py
"""
All-in-MCP FastMCP Proxy Server

This server proxies requests to the APaper academic research module
and can be extended to proxy to other MCP servers.
"""

from pathlib import Path
from fastmcp import FastMCP

# Initialize the main proxy server
app = FastMCP("all-in-mcp")


# Import and register APaper tools
try:
    import sys
    from pathlib import Path
    
    # Add the parent directory to path to import apaper
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.insert(0, str(parent_dir))
    
    from apaper.platforms import (
        IACRSearcher,
        CryptoBibSearcher, 
        CrossrefSearcher,
        GoogleScholarSearcher
    )
    from apaper.utils.pdf_reader import read_pdf
    
    # Initialize searchers
    iacr_searcher = IACRSearcher()
    cryptobib_searcher = CryptoBibSearcher(cache_dir="./downloads")
    crossref_searcher = CrossrefSearcher()
    google_scholar_searcher = GoogleScholarSearcher()
    
    # Academic paper search tools
    @app.tool()
    def search_iacr_papers(
        query: str,
        max_results: int = 10,
        fetch_details: bool = True,
        year_min: int | None = None,
        year_max: int | None = None,
    ) -> str:
        """Search academic papers from IACR ePrint Archive"""
        try:
            papers = iacr_searcher.search(
                query, max_results=max_results, fetch_details=fetch_details,
                year_min=year_min, year_max=year_max
            )
            
            if not papers:
                year_filter_msg = ""
                if year_min or year_max:
                    year_range = f" ({year_min or 'earliest'}-{year_max or 'latest'})"
                    year_filter_msg = f" in year range{year_range}"
                return f"No papers found for query: {query}{year_filter_msg}"
            
            result_lines = [f"Found {len(papers)} IACR papers for query '{query}':\n"]
            
            for i, paper in enumerate(papers, 1):
                result_lines.append(f"{i}. **{paper.title}**")
                result_lines.append(f"   - Paper ID: {paper.paper_id}")
                result_lines.append(f"   - Authors: {', '.join(paper.authors)}")
                result_lines.append(f"   - URL: {paper.url}")
                result_lines.append(f"   - PDF: {paper.pdf_url}")
                if paper.categories:
                    result_lines.append(f"   - Categories: {', '.join(paper.categories)}")
                if paper.keywords:
                    result_lines.append(f"   - Keywords: {', '.join(paper.keywords)}")
                if paper.abstract:
                    result_lines.append(f"   - Abstract: {paper.abstract}")
                result_lines.append("")
            
            return "\n".join(result_lines)
        except Exception as e:
            return f"Error searching IACR papers: {str(e)}"

    @app.tool()
    def download_iacr_paper(paper_id: str, save_path: str = "./downloads") -> str:
        """Download PDF of an IACR ePrint paper"""
        try:
            result = iacr_searcher.download_pdf(paper_id, save_path)
            if result.startswith(("Error", "Failed")):
                return f"Download failed: {result}"
            else:
                return f"PDF downloaded successfully to: {result}"
        except Exception as e:
            return f"Error downloading IACR paper: {str(e)}"

    @app.tool() 
    def read_iacr_paper(
        paper_id: str,
        save_path: str = "./downloads",
        start_page: int | None = None,
        end_page: int | None = None,
    ) -> str:
        """Read and extract text content from an IACR ePrint paper PDF"""
        try:
            result = iacr_searcher.read_paper(
                paper_id, save_path, start_page=start_page, end_page=end_page
            )
            if result.startswith("Error"):
                return result
            elif len(result) > 5000:
                return result[:5000] + f"\n\n... [Text truncated. Full text is {len(result)} characters long]"
            else:
                return result
        except Exception as e:
            return f"Error reading IACR paper: {str(e)}"

    @app.tool()
    def search_cryptobib_papers(
        query: str,
        max_results: int = 10,
        return_bibtex: bool = False,
        force_download: bool = False,
        year_min: int | None = None,
        year_max: int | None = None,
    ) -> str:
        """Search CryptoBib bibliography database for cryptography papers"""
        try:
            if return_bibtex:
                bibtex_entries = cryptobib_searcher.search_bibtex(
                    query, max_results, force_download=force_download,
                    year_min=year_min, year_max=year_max
                )
                if not bibtex_entries:
                    return f"No BibTeX entries found for query: {query}"
                
                result_lines = [f"Found {len(bibtex_entries)} BibTeX entries for query '{query}':\n"]
                for i, entry in enumerate(bibtex_entries, 1):
                    result_lines.append(f"Entry {i}:\n```bibtex\n{entry}\n```\n")
                return "\n".join(result_lines)
            else:
                papers = cryptobib_searcher.search(
                    query, max_results, force_download=force_download,
                    year_min=year_min, year_max=year_max
                )
                if not papers:
                    return f"No papers found for query: {query}"
                
                result_lines = [f"Found {len(papers)} CryptoBib papers for query '{query}':\n"]
                for i, paper in enumerate(papers, 1):
                    result_lines.append(f"{i}. **{paper.title}**")
                    result_lines.append(f"   - Entry Key: {paper.paper_id}")
                    result_lines.append(f"   - Authors: {', '.join(paper.authors)}")
                    if paper.extra and "venue" in paper.extra:
                        result_lines.append(f"   - Venue: {paper.extra['venue']}")
                    if paper.published_date and paper.published_date.year > 1900:
                        result_lines.append(f"   - Year: {paper.published_date.year}")
                    if paper.doi:
                        result_lines.append(f"   - DOI: {paper.doi}")
                    result_lines.append("")
                return "\n".join(result_lines)
        except Exception as e:
            return f"Error searching CryptoBib papers: {str(e)}"

    @app.tool()
    def search_google_scholar_papers(
        query: str,
        max_results: int = 10,
        year_low: int | None = None,
        year_high: int | None = None,
    ) -> str:
        """Search academic papers from Google Scholar"""
        try:
            papers = google_scholar_searcher.search(
                query, max_results=max_results, year_low=year_low, year_high=year_high
            )
            if not papers:
                return f"No papers found for query: {query}"
            
            result_lines = [f"Found {len(papers)} Google Scholar papers for query '{query}':\n"]
            for i, paper in enumerate(papers, 1):
                result_lines.append(f"{i}. **{paper.title}**")
                result_lines.append(f"   - Authors: {', '.join(paper.authors)}")
                if paper.citations > 0:
                    result_lines.append(f"   - Citations: {paper.citations}")
                if paper.published_date and paper.published_date.year > 1900:
                    result_lines.append(f"   - Year: {paper.published_date.year}")
                if paper.url:
                    result_lines.append(f"   - URL: {paper.url}")
                if paper.abstract:
                    abstract_preview = paper.abstract[:300] + "..." if len(paper.abstract) > 300 else paper.abstract
                    result_lines.append(f"   - Abstract: {abstract_preview}")
                result_lines.append("")
            return "\n".join(result_lines)
        except Exception as e:
            return f"Error searching Google Scholar: {str(e)}"

    @app.tool()
    def search_crossref_papers(
        query: str,
        max_results: int = 10,
        year_min: int | None = None,
        year_max: int | None = None,
        sort_by: str = "relevance",
    ) -> str:
        """Search academic papers from Crossref database"""
        try:
            papers = crossref_searcher.search(
                query, max_results=max_results, year_min=year_min,
                year_max=year_max, sort_by=sort_by
            )
            if not papers:
                return f"No papers found for query: {query}"
            
            result_lines = [f"Found {len(papers)} Crossref papers for query '{query}':\n"]
            for i, paper in enumerate(papers, 1):
                result_lines.append(f"{i}. **{paper.title}**")
                result_lines.append(f"   - Authors: {', '.join(paper.authors)}")
                if paper.doi:
                    result_lines.append(f"   - DOI: {paper.doi}")
                if paper.citations > 0:
                    result_lines.append(f"   - Citations: {paper.citations}")
                if paper.published_date and paper.published_date.year > 1900:
                    result_lines.append(f"   - Year: {paper.published_date.year}")
                if paper.extra and paper.extra.get("journal"):
                    result_lines.append(f"   - Journal: {paper.extra['journal']}")
                if paper.url:
                    result_lines.append(f"   - URL: {paper.url}")
                result_lines.append("")
            return "\n".join(result_lines)
        except Exception as e:
            return f"Error searching Crossref: {str(e)}"

    @app.tool()
    def read_pdf(
        pdf_source: str,
        start_page: int | None = None,
        end_page: int | None = None,
    ) -> str:
        """Read and extract text content from a PDF file (local or online)"""
        try:
            from apaper.utils.pdf_reader import read_pdf as _read_pdf
            result = _read_pdf(pdf_source, start_page=start_page, end_page=end_page)
            return result
        except Exception as e:
            return f"Error reading PDF from {pdf_source}: {str(e)}"

except ImportError as e:
    print(f"Warning: Could not import APaper functionality: {e}")
    
    # Fallback tools when APaper is not available
    @app.tool()
    def search_iacr_papers(query: str, **kwargs) -> str:
        """Search academic papers from IACR ePrint Archive (APaper not available)"""
        return f"APaper module not available. Cannot search for: {query}"


@app.tool()
def proxy_status() -> str:
    """Get the status of the all-in-mcp proxy server"""
    return "All-in-MCP proxy server is running with FastMCP architecture"


@app.tool()
def list_tools() -> str:
    """List all available tools in the proxy server"""
    tools = [
        "Academic Paper Search Tools:",
        "- search_iacr_papers: Search IACR ePrint Archive",
        "- download_iacr_paper: Download IACR papers",
        "- read_iacr_paper: Read IACR paper content", 
        "- search_cryptobib_papers: Search CryptoBib database",
        "- search_google_scholar_papers: Search Google Scholar",
        "- search_crossref_papers: Search Crossref database",
        "- read_pdf: Read PDF files from local or online sources",
        "",
        "Proxy Management Tools:",
        "- proxy_status: Check proxy server status",
        "- list_tools: List all available tools",
    ]
    return "\n".join(tools)


def main():
    """Main entry point for the all-in-mcp proxy server."""
    app.run()


if __name__ == "__main__":
    main()