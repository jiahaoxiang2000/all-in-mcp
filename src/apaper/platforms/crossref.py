# all_in_mcp/academic_platforms/crossref.py
import logging
from datetime import datetime
from typing import Optional
from urllib.parse import quote_plus

import httpx

from ..models.paper import Paper
from .base import PaperSource

logger = logging.getLogger(__name__)


class CrossrefSearcher(PaperSource):
    """Crossref API paper search implementation"""

    BASE_URL = "https://api.crossref.org"
    WORKS_ENDPOINT = f"{BASE_URL}/works"

    def __init__(self, email: Optional[str] = None):
        """
        Initialize Crossref searcher

        Args:
            email: Optional email for polite API usage (recommended by Crossref)
        """
        self.email = email
        self.client = httpx.Client(timeout=30.0)

    def _get_headers(self) -> dict:
        """Get headers for API requests"""
        headers = {
            "User-Agent": "all-in-mcp/0.1.0 (https://github.com/user/all-in-mcp)"
        }
        if self.email:
            headers["User-Agent"] += f" (mailto:{self.email})"
        return headers

    def _parse_date(self, date_parts: list) -> Optional[datetime]:
        """Parse Crossref date parts into datetime"""
        if not date_parts or not isinstance(date_parts, list):
            return None

        try:
            # Crossref provides date as [[year, month, day]] or [[year, month]] or [[year]]
            if len(date_parts) > 0 and isinstance(date_parts[0], list):
                parts = date_parts[0]
                year = parts[0] if len(parts) > 0 else 1
                month = parts[1] if len(parts) > 1 else 1
                day = parts[2] if len(parts) > 2 else 1
                return datetime(year, month, day)
        except (ValueError, IndexError, TypeError):
            pass
        return None

    def _extract_authors(self, authors_data: list) -> list[str]:
        """Extract author names from Crossref author data"""
        authors = []
        for author in authors_data or []:
            if isinstance(author, dict):
                given = author.get("given", "")
                family = author.get("family", "")
                if given and family:
                    authors.append(f"{given} {family}")
                elif family:
                    authors.append(family)
                elif given:
                    authors.append(given)
        return authors

    def _parse_work(self, work: dict) -> Optional[Paper]:
        """Parse a single work from Crossref API response"""
        try:
            # Extract basic information
            title_list = work.get("title", [])
            title = title_list[0] if title_list else ""

            if not title:
                return None

            doi = work.get("DOI", "")
            paper_id = doi or work.get("URL", "")

            # Extract authors
            authors = self._extract_authors(work.get("author", []))

            # Extract abstract
            abstract = work.get("abstract", "")
            if abstract:
                # Remove HTML tags if present
                import re

                abstract = re.sub(r"<[^>]+>", "", abstract)

            # Extract publication date
            published_date = (
                self._parse_date(work.get("published-print", {}).get("date-parts"))
                or self._parse_date(work.get("published-online", {}).get("date-parts"))
                or self._parse_date(work.get("created", {}).get("date-parts"))
            )

            # Extract URLs
            url = work.get("URL", "")
            pdf_url = ""

            # Look for PDF in links
            links = work.get("link", [])
            for link in links:
                if link.get("content-type") == "application/pdf":
                    pdf_url = link.get("URL", "")
                    break

            # Extract additional metadata
            container_title = work.get("container-title", [])
            journal = container_title[0] if container_title else ""

            volume = work.get("volume", "")
            issue = work.get("issue", "")
            pages = work.get("page", "")

            # Extract categories/subjects
            categories = []
            subjects = work.get("subject", [])
            if subjects:
                categories.extend(subjects)

            # Citation count (if available)
            citations = work.get("is-referenced-by-count", 0)

            # Build extra metadata
            extra = {
                "journal": journal,
                "volume": volume,
                "issue": issue,
                "pages": pages,
                "type": work.get("type", ""),
                "publisher": work.get("publisher", ""),
                "issn": work.get("ISSN", []),
                "isbn": work.get("ISBN", []),
            }

            # Remove empty values from extra
            extra = {k: v for k, v in extra.items() if v}

            return Paper(
                paper_id=paper_id,
                title=title,
                authors=authors,
                abstract=abstract,
                doi=doi,
                published_date=published_date or datetime(1900, 1, 1),
                pdf_url=pdf_url,
                url=url,
                source="crossref",
                categories=categories,
                citations=citations,
                extra=extra,
            )

        except Exception as e:
            logger.error(f"Error parsing Crossref work: {e}")
            return None

    def search(
        self,
        query: str,
        max_results: int = 10,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        sort_by: str = "relevance",
        **kwargs,
    ) -> list[Paper]:
        """
        Search for papers using Crossref API

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            year_min: Minimum publication year
            year_max: Maximum publication year
            sort_by: Sort order (relevance, published, indexed, updated)
        """
        if not query.strip():
            return []

        try:
            params = {
                "query": query,
                "rows": min(max_results, 1000),  # Crossref max is 1000
                "sort": sort_by,
                "select": "DOI,title,author,abstract,published-print,published-online,created,URL,container-title,volume,issue,page,subject,is-referenced-by-count,type,publisher,ISSN,ISBN,link",
            }

            # Add year filters if specified
            filters = []
            if year_min:
                filters.append(f"from-pub-date:{year_min}")
            if year_max:
                filters.append(f"until-pub-date:{year_max}")

            if filters:
                params["filter"] = ",".join(filters)

            response = self.client.get(
                self.WORKS_ENDPOINT, params=params, headers=self._get_headers()
            )
            response.raise_for_status()

            data = response.json()
            works = data.get("message", {}).get("items", [])

            papers = []
            for work in works:
                paper = self._parse_work(work)
                if paper:
                    papers.append(paper)

            return papers[:max_results]

        except Exception as e:
            logger.error(f"Error searching Crossref: {e}")
            return []

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        """
        Not implemented: Download PDF for a paper (limited functionality for Crossref)
        """
        return "Crossref does not provide a direct way to download PDFs. Use the paper's URL or DOI to access the publisher's site for PDF downloads if available."

    def read_paper(self, paper_id: str, save_path: str, start_page: int | None = None, end_page: int | None = None) -> str:
        """
        crossref doesn't provide a direct way to read paper text.
        
        Args:
            paper_id: Paper identifier
            save_path: Directory where papers are stored
            start_page: Starting page number (1-indexed, inclusive). Defaults to 1.
            end_page: Ending page number (1-indexed, inclusive). Defaults to last page.
        """
        return "Crossref does not provide a direct way to read paper text. Use the download_pdf method to get the PDF if available."

    def search_by_doi(self, doi: str) -> Optional[Paper]:
        """Search for a specific paper by DOI"""
        try:
            work_url = f"{self.WORKS_ENDPOINT}/{quote_plus(doi)}"
            response = self.client.get(work_url, headers=self._get_headers())
            response.raise_for_status()

            data = response.json()
            work = data.get("message", {})

            return self._parse_work(work)

        except Exception as e:
            logger.error(f"Error searching by DOI {doi}: {e}")
            return None

    def __del__(self):
        """Clean up HTTP client"""
        if hasattr(self, "client"):
            self.client.close()
