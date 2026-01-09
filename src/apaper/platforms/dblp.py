# apaper/platforms/dblp.py
"""DBLP bibliography search and BibTeX export implementation.

This module provides access to the DBLP computer science bibliography database
for searching publications and exporting BibTeX entries.

Reference: https://dblp.org/
Based on: https://github.com/szeider/mcp-dblp
"""

import logging
import re
from typing import Any

import requests

from ..models.paper import Paper

logger = logging.getLogger(__name__)

# Default timeout for all HTTP requests
REQUEST_TIMEOUT = 10  # seconds

# Headers for DBLP API requests
HEADERS = {
    "User-Agent": "apaper/1.0 (https://github.com/jiahaoxiang2000/all-in-mcp)",
    "Accept": "application/json",
}


class DBLPSearcher:
    """DBLP (https://dblp.org/) bibliography search and BibTeX export implementation."""

    def __init__(self) -> None:
        """Initialize the DBLP searcher."""
        self.bibtex_buffer: dict[str, str] = {}

    def search(
        self,
        query: str,
        max_results: int = 10,
        year_from: int | None = None,
        year_to: int | None = None,
        venue_filter: str | None = None,
        include_bibtex: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Search DBLP for publications.

        Args:
            query: Search query string (supports boolean 'and'/'or' operators)
            max_results: Maximum number of results to return (default: 10)
            year_from: Lower bound for publication year
            year_to: Upper bound for publication year
            venue_filter: Case-insensitive substring filter for venues
            include_bibtex: Whether to include BibTeX entries in results

        Returns:
            List of publication dictionaries with title, authors, venue, year, etc.
        """
        query_lower = query.lower()
        results = []

        # Handle OR queries
        if " or " in query_lower:
            subqueries = [q.strip() for q in query_lower.split(" or ") if q.strip()]
            seen = set()
            for q in subqueries:
                for pub in self._fetch_publications(q, max_results):
                    identifier = (pub.get("title"), pub.get("year"))
                    if identifier not in seen:
                        results.append(pub)
                        seen.add(identifier)
        else:
            results = self._fetch_publications(query, max_results)

        # Apply filters
        filtered_results = []
        for result in results:
            # Year filter
            if year_from or year_to:
                year = result.get("year")
                if year:
                    try:
                        year = int(year)
                        if (year_from and year < year_from) or (
                            year_to and year > year_to
                        ):
                            continue
                    except (ValueError, TypeError):
                        pass

            # Venue filter
            if venue_filter:
                venue = result.get("venue", "")
                if venue_filter.lower() not in venue.lower():
                    continue

            filtered_results.append(result)

        filtered_results = filtered_results[:max_results]

        # Fetch BibTeX entries if requested
        if include_bibtex:
            bibtex_results = []
            for result in filtered_results:
                if "dblp_key" in result and result["dblp_key"]:
                    bibtex = self.fetch_bibtex_entry(result["dblp_key"])
                    if bibtex:
                        bibtex_results.append(
                            {"bibtex": bibtex, "dblp_key": result["dblp_key"]}
                        )
            return bibtex_results

        return filtered_results

    def _fetch_publications(
        self, single_query: str, max_results: int
    ) -> list[dict[str, Any]]:
        """Fetch publications for a single query string."""
        results = []
        try:
            url = "https://dblp.org/search/publ/api"
            params = {"q": single_query, "format": "json", "h": max_results}
            response = requests.get(
                url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()

            hits = data.get("result", {}).get("hits", {})
            total = int(hits.get("@total", "0"))
            logger.info(f"Found {total} results for query: {single_query}")

            if total > 0:
                publications = hits.get("hit", [])
                if not isinstance(publications, list):
                    publications = [publications]

                for pub in publications:
                    info = pub.get("info", {})

                    # Extract authors
                    authors = []
                    authors_data = info.get("authors", {}).get("author", [])
                    if not isinstance(authors_data, list):
                        authors_data = [authors_data]
                    for author in authors_data:
                        if isinstance(author, dict):
                            authors.append(author.get("text", ""))
                        else:
                            authors.append(str(author))

                    # Extract DBLP key
                    dblp_url = info.get("url", "")
                    dblp_key = ""
                    if dblp_url:
                        dblp_key = dblp_url.replace("https://dblp.org/rec/", "")
                    elif "key" in pub:
                        dblp_key = pub.get("key", "").replace("dblp:", "")
                    else:
                        dblp_key = pub.get("@id", "").replace("dblp:", "")

                    result = {
                        "title": info.get("title", ""),
                        "authors": authors,
                        "venue": info.get("venue", ""),
                        "year": int(info.get("year", 0)) if info.get("year") else None,
                        "type": info.get("type", ""),
                        "doi": info.get("doi", ""),
                        "ee": info.get("ee", ""),
                        "url": info.get("url", ""),
                        "dblp_key": dblp_key,
                    }
                    results.append(result)

        except requests.exceptions.Timeout:
            logger.error(
                f"Timeout error searching DBLP after {REQUEST_TIMEOUT} seconds"
            )
            results.append(
                {
                    "title": f"ERROR: Query '{single_query}' timed out after {REQUEST_TIMEOUT} seconds",
                    "authors": [],
                    "venue": "Error",
                    "year": None,
                    "error": f"Timeout after {REQUEST_TIMEOUT} seconds",
                }
            )
        except Exception as e:
            logger.error(f"Error searching DBLP: {e}")
            results.append(
                {
                    "title": f"ERROR: DBLP API error for query '{single_query}': {str(e)}",
                    "authors": [],
                    "venue": "Error",
                    "year": None,
                    "error": str(e),
                }
            )

        return results

    def fetch_bibtex_entry(self, dblp_key: str) -> str:
        """
        Fetch BibTeX entry from DBLP by key.

        Args:
            dblp_key: DBLP publication key (e.g., 'conf/nips/VaswaniSPUJGKP17')

        Returns:
            BibTeX entry string, or empty string if not found
        """
        try:
            if not dblp_key or dblp_key.isspace():
                logger.warning("Empty or invalid DBLP key provided")
                return ""

            # Try multiple URL formats
            urls_to_try = [f"https://dblp.org/rec/{dblp_key}.bib"]

            if ":" in dblp_key:
                clean_key = dblp_key.replace(":", "/")
                urls_to_try.append(f"https://dblp.org/rec/{clean_key}.bib")

            for url in urls_to_try:
                logger.info(f"Fetching BibTeX from: {url}")
                response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)

                if response.status_code == 200:
                    bibtex = response.text
                    if not bibtex or bibtex.isspace():
                        continue
                    return bibtex

            logger.warning(f"Failed to fetch BibTeX for key: {dblp_key}")
            return ""

        except requests.exceptions.Timeout:
            logger.error(
                f"Timeout fetching BibTeX for {dblp_key} after {REQUEST_TIMEOUT} seconds"
            )
            return f"% Error: Timeout fetching BibTeX for {dblp_key}"
        except Exception as e:
            logger.error(f"Error fetching BibTeX for {dblp_key}: {str(e)}")
            return f"% Error: {str(e)}"

    def search_to_papers(
        self,
        query: str,
        max_results: int = 10,
        year_from: int | None = None,
        year_to: int | None = None,
        venue_filter: str | None = None,
    ) -> list[Paper]:
        """
        Search DBLP and return results as Paper objects.

        This method is provided for consistency with other platform searchers.

        Args:
            query: Search query string
            max_results: Maximum number of results
            year_from: Lower bound for publication year
            year_to: Upper bound for publication year
            venue_filter: Case-insensitive substring filter for venues

        Returns:
            List of Paper objects
        """
        from datetime import datetime

        results = self.search(
            query,
            max_results=max_results,
            year_from=year_from,
            year_to=year_to,
            venue_filter=venue_filter,
            include_bibtex=False,
        )

        papers = []
        for result in results:
            if result.get("error"):
                continue

            year = result.get("year")
            published_date = datetime(year, 1, 1) if year else datetime(1900, 1, 1)

            paper = Paper(
                paper_id=result.get("dblp_key", ""),
                title=result.get("title", ""),
                authors=result.get("authors", []),
                abstract="",  # DBLP doesn't provide abstracts
                url=result.get("url", ""),
                pdf_url=result.get("ee", ""),  # Electronic edition URL
                published_date=published_date,
                updated_date=None,
                source="dblp",
                categories=[result.get("type", "")] if result.get("type") else [],
                keywords=[],
                doi=result.get("doi", ""),
                citations=0,
                extra={
                    "venue": result.get("venue", ""),
                    "dblp_key": result.get("dblp_key", ""),
                },
            )
            papers.append(paper)

        return papers
