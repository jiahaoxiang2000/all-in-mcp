# apaper/platforms/iacr.py
import logging
import os
import random
from datetime import datetime
from typing import ClassVar

import requests
from bs4 import BeautifulSoup

from ..models.paper import Paper
from .base import PaperSource

logger = logging.getLogger(__name__)


class IACRSearcher(PaperSource):
    """IACR ePrint Archive paper search implementation"""

    IACR_SEARCH_URL = "https://eprint.iacr.org/search"
    IACR_BASE_URL = "https://eprint.iacr.org"
    BROWSERS: ClassVar[list[str]] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    ]

    def __init__(self):
        self._setup_session()

    def _setup_session(self):
        """Initialize session with random user agent"""
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": random.choice(self.BROWSERS),
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    def _parse_date(self, date_str: str) -> datetime | None:
        """Parse date from IACR format (e.g., '2025-06-02')"""
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d")
        except ValueError:
            logger.warning(f"Could not parse date: {date_str}")
            return None

    def _parse_paper(self, item, fetch_details: bool = True) -> Paper | None:
        """Parse single paper entry from IACR HTML and optionally fetch detailed info"""
        try:
            # Extract paper ID from the search result
            header_div = item.find("div", class_="d-flex")
            if not header_div:
                return None

            # Get paper ID from the link
            paper_link = header_div.find("a", class_="paperlink")
            if not paper_link:
                return None

            paper_id = paper_link.get_text(strip=True)  # e.g., "2025/1014"

            if fetch_details:
                # Fetch detailed information for this paper
                logger.info(f"Fetching detailed info for paper {paper_id}")
                detailed_paper = self.get_paper_details(paper_id)
                if detailed_paper:
                    return detailed_paper
                else:
                    logger.warning(
                        f"Could not fetch details for {paper_id}, falling back to search result parsing"
                    )

            # Fallback: parse from search results if detailed fetch fails or is disabled
            paper_url = self.IACR_BASE_URL + paper_link["href"]

            # Get PDF URL
            pdf_link = header_div.find("a", href=True, string="(PDF)")
            pdf_url = self.IACR_BASE_URL + pdf_link["href"] if pdf_link else ""

            # Get last updated date
            last_updated_elem = header_div.find("small", class_="ms-auto")
            updated_date = None
            if last_updated_elem:
                date_text = last_updated_elem.get_text(strip=True)
                if "Last updated:" in date_text:
                    date_str = date_text.replace("Last updated:", "").strip()
                    updated_date = self._parse_date(date_str)

            # Get content from the second div
            content_div = item.find("div", class_="ms-md-4")
            if not content_div:
                return None

            # Extract title
            title_elem = content_div.find("strong")
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract authors
            authors_elem = content_div.find("span", class_="fst-italic")
            authors = []
            if authors_elem:
                authors_text = authors_elem.get_text(strip=True)
                authors = [author.strip() for author in authors_text.split(",")]

            # Extract category
            category_elem = content_div.find("small", class_="badge")
            categories = []
            if category_elem:
                category_text = category_elem.get_text(strip=True)
                categories = [category_text]

            # Extract abstract
            abstract_elem = content_div.find("p", class_="search-abstract")
            abstract = abstract_elem.get_text(strip=True) if abstract_elem else ""

            # Create paper object with search result data
            published_date = updated_date if updated_date else datetime(1900, 1, 1)

            return Paper(
                paper_id=paper_id,
                title=title,
                authors=authors,
                abstract=abstract,
                url=paper_url,
                pdf_url=pdf_url,
                published_date=published_date,
                updated_date=updated_date,
                source="iacr",
                categories=categories,
                keywords=[],
                doi="",
                citations=0,
            )

        except Exception as e:
            logger.warning(f"Failed to parse IACR paper: {e}")
            return None

    def search(
        self,
        query: str,
        max_results: int = 10,
        fetch_details: bool = True,
        year_min: int | None = None,
        year_max: int | None = None,
    ) -> list[Paper]:
        """
        Search IACR ePrint Archive

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            fetch_details: Whether to fetch detailed information for each paper (slower but more complete)
            year_min: Minimum publication year (revised after)
            year_max: Maximum publication year (revised before)

        Returns:
            List[Paper]: List of paper objects
        """
        papers = []

        try:
            # Construct search parameters
            params: dict[str, str | int] = {"q": query}
            if year_min:
                params["revisedafter"] = year_min
            if year_max:
                params["revisedbefore"] = year_max

            # Make request
            response = self.session.get(self.IACR_SEARCH_URL, params=params)

            if response.status_code != 200:
                logger.error(f"IACR search failed with status {response.status_code}")
                return papers

            # Parse results
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all paper entries - they are divs with class "mb-4"
            results = soup.find_all("div", class_="mb-4")

            if not results:
                logger.info("No results found for the query")
                return papers

            # Process each result
            for i, item in enumerate(results):
                if len(papers) >= max_results:
                    break

                logger.info(
                    f"Processing paper {i + 1}/{min(len(results), max_results)}"
                )
                paper = self._parse_paper(item, fetch_details=fetch_details)
                if paper:
                    papers.append(paper)

        except Exception as e:
            logger.error(f"IACR search error: {e}")

        return papers[:max_results]

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        """
        Download PDF from IACR ePrint Archive

        Args:
            paper_id: IACR paper ID (e.g., "2025/1014")
            save_path: Path to save the PDF

        Returns:
            str: Path to downloaded file or error message
        """
        try:
            os.makedirs(save_path, exist_ok=True)
            pdf_url = f"{self.IACR_BASE_URL}/{paper_id}.pdf"

            response = self.session.get(pdf_url)

            if response.status_code == 200:
                filename = f"{save_path}/iacr_{paper_id.replace('/', '_')}.pdf"
                with open(filename, "wb") as f:
                    f.write(response.content)
                return filename
            else:
                return f"Failed to download PDF: HTTP {response.status_code}"

        except Exception as e:
            logger.error(f"PDF download error: {e}")
            return f"Error downloading PDF: {e}"

    def get_paper_details(self, paper_id: str) -> Paper | None:
        """
        Fetch detailed information for a specific IACR paper

        Args:
            paper_id: IACR paper ID (e.g., "2009/101") or full URL

        Returns:
            Paper: Detailed paper object with full metadata
        """
        try:
            # Handle both paper ID and full URL
            if paper_id.startswith("http"):
                paper_url = paper_id
                # Extract paper ID from URL
                parts = paper_url.split("/")
                if len(parts) >= 2:
                    paper_id = f"{parts[-2]}/{parts[-1]}"
            else:
                paper_url = f"{self.IACR_BASE_URL}/{paper_id}"

            # Make request
            response = self.session.get(paper_url)

            if response.status_code != 200:
                logger.error(
                    f"Failed to fetch paper details: HTTP {response.status_code}"
                )
                return None

            # Parse the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title from h3 element
            title = ""
            title_elem = soup.find("h3", class_="mb-3")
            if title_elem:
                title = title_elem.get_text(strip=True)

            # Extract authors from the italic paragraph
            authors = []
            author_elem = soup.find("p", class_="fst-italic")
            if author_elem:
                author_text = author_elem.get_text(strip=True)
                # Split by " and " to get individual authors
                authors = [
                    author.strip()
                    for author in author_text.replace(" and ", ",").split(",")
                ]

            # Extract abstract using multiple strategies
            abstract = ""

            # Look for paragraph with white-space: pre-wrap style (current method)
            abstract_p = soup.find("p", style="white-space: pre-wrap;")
            if abstract_p:
                abstract = abstract_p.get_text(strip=True)

            # Extract metadata using a simpler, safer approach
            publication_info = ""
            keywords = []
            history_entries = []
            last_updated = None

            # Extract publication info
            page_text = soup.get_text()
            lines = page_text.split("\n")

            # Find publication info
            for i, line in enumerate(lines):
                if "Publication info" in line and i + 1 < len(lines):
                    publication_info = lines[i + 1].strip()
                    break

            # Find keywords using CSS selector for keyword badges
            try:
                keyword_elements = soup.select("a.badge.bg-secondary.keyword")
                keywords = [elem.get_text(strip=True) for elem in keyword_elements]
            except Exception:
                keywords = []

            # Find history entries
            history_found = False
            for _i, line in enumerate(lines):
                if "History" in line and ":" not in line:
                    history_found = True
                    continue
                elif (
                    history_found
                    and ":" in line
                    and not line.strip().startswith("Short URL")
                ):
                    history_entries.append(line.strip())
                    # Try to extract the last updated date from the first history entry
                    if not last_updated:
                        date_str = line.split(":")[0].strip()
                        try:
                            last_updated = datetime.strptime(date_str, "%Y-%m-%d")
                        except ValueError:
                            pass
                elif history_found and (
                    line.strip().startswith("Short URL")
                    or line.strip().startswith("License")
                ):
                    break

            # Combine history entries
            history = "; ".join(history_entries) if history_entries else ""

            # Construct PDF URL
            pdf_url = f"{self.IACR_BASE_URL}/{paper_id}.pdf"

            # Use last updated date or current date as published date
            published_date = last_updated if last_updated else datetime.now()

            return Paper(
                paper_id=paper_id,
                title=title,
                authors=authors,
                abstract=abstract,
                url=paper_url,
                pdf_url=pdf_url,
                published_date=published_date,
                updated_date=last_updated,
                source="iacr",
                categories=[],
                keywords=keywords,
                doi="",
                citations=0,
                extra={"publication_info": publication_info, "history": history},
            )

        except Exception as e:
            logger.error(f"Error fetching paper details for {paper_id}: {e}")
            return None
