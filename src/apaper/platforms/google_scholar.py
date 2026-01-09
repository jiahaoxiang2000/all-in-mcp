# all_in_mcp/academic_platforms/google_scholar.py
import logging
import random
import time
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from ..models.paper import Paper
from .base import PaperSource

logger = logging.getLogger(__name__)


class GoogleScholarSearcher(PaperSource):
    """Google Scholar paper search implementation"""

    SCHOLAR_URL = "https://scholar.google.com/scholar"
    BROWSERS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]

    def __init__(self):
        """Initialize Google Scholar searcher"""
        self._setup_session()

    def _setup_session(self):
        """Initialize session with random user agent"""
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": random.choice(self.BROWSERS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def _extract_year(self, text: str) -> Optional[int]:
        """Extract publication year from text"""
        words = text.replace(",", " ").replace("-", " ").split()
        for word in words:
            if word.isdigit() and 1900 <= int(word) <= datetime.now().year:
                return int(word)
        return None

    def _extract_citations(self, item) -> int:
        """Extract citation count from paper item"""
        try:
            citation_elem = item.find("div", class_="gs_fl")
            if citation_elem:
                citation_link = citation_elem.find(
                    "a", string=lambda text: text and "Cited by" in text
                )
                if citation_link:
                    citation_text = citation_link.get_text()
                    # Extract number from "Cited by X" text
                    citation_num = "".join(filter(str.isdigit, citation_text))
                    return int(citation_num) if citation_num else 0
            return 0
        except Exception:
            return 0

    def _parse_paper(self, item) -> Optional[Paper]:
        """Parse a single paper entry from HTML"""
        try:
            # Extract main paper elements
            title_elem = item.find("h3", class_="gs_rt")
            info_elem = item.find("div", class_="gs_a")
            abstract_elem = item.find("div", class_="gs_rs")

            if not title_elem or not info_elem:
                return None

            # Process title and URL
            title_text = title_elem.get_text(strip=True)
            # Remove common prefixes
            title = (
                title_text.replace("[PDF]", "")
                .replace("[HTML]", "")
                .replace("[BOOK]", "")
                .strip()
            )

            link = title_elem.find("a", href=True)
            url = link["href"] if link else ""

            # Process author and publication info
            info_text = info_elem.get_text()
            info_parts = info_text.split(" - ")

            # Extract authors (usually the first part before the first dash)
            authors_text = info_parts[0] if info_parts else ""
            authors = [a.strip() for a in authors_text.split(",") if a.strip()]

            # Extract year from the info text
            year = self._extract_year(info_text)

            # Extract abstract
            abstract = abstract_elem.get_text(strip=True) if abstract_elem else ""

            # Extract citations
            citations = self._extract_citations(item)

            # Generate a paper ID based on the URL or title
            paper_id = f"gs_{abs(hash(url if url else title))}"

            # Create paper object
            return Paper(
                paper_id=paper_id,
                title=title,
                authors=authors,
                abstract=abstract,
                url=url,
                pdf_url="",  # Google Scholar doesn't provide direct PDF links
                published_date=datetime(year, 1, 1) if year else datetime.now(),
                updated_date=None,
                source="google_scholar",
                categories=[],
                keywords=[],
                doi="",
                citations=citations,
                references=[],
                extra={"info_text": info_text},
            )
        except Exception as e:
            logger.warning(f"Failed to parse paper: {e}")
            return None

    def search(self, query: str, max_results: int = 10, **kwargs) -> list[Paper]:
        """
        Search Google Scholar for papers

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            **kwargs: Additional search parameters (e.g., year_low, year_high)

        Returns:
            List of Paper objects
        """
        papers = []
        start = 0
        results_per_page = min(10, max_results)

        # Extract additional parameters
        year_low = kwargs.get("year_low")
        year_high = kwargs.get("year_high")

        while len(papers) < max_results:
            try:
                # Construct search parameters
                params = {
                    "q": query,
                    "start": start,
                    "hl": "en",
                    "as_sdt": "0,5",  # Include articles and citations
                    "num": results_per_page,
                }

                # Add year filters if provided
                if year_low:
                    params["as_ylo"] = year_low
                if year_high:
                    params["as_yhi"] = year_high

                # Make request with random delay to avoid rate limiting
                time.sleep(random.uniform(1.0, 3.0))
                response = self.session.get(self.SCHOLAR_URL, params=params, timeout=30)

                if response.status_code != 200:
                    logger.error(f"Search failed with status {response.status_code}")
                    break

                # Parse results
                soup = BeautifulSoup(response.text, "html.parser")
                results = soup.find_all("div", class_="gs_ri")

                if not results:
                    logger.info("No more results found")
                    break

                # Process each result
                for item in results:
                    if len(papers) >= max_results:
                        break

                    paper = self._parse_paper(item)
                    if paper:
                        papers.append(paper)

                start += results_per_page

            except requests.exceptions.RequestException as e:
                logger.error(f"Network error during search: {e}")
                break
            except Exception as e:
                logger.error(f"Search error: {e}")
                break

        return papers[:max_results]

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        """
        Google Scholar doesn't support direct PDF downloads

        Args:
            paper_id: Paper identifier
            save_path: Directory to save the PDF

        Returns:
            Error message explaining limitation

        Raises:
            NotImplementedError: Always raises this error
        """
        raise NotImplementedError(
            "Google Scholar doesn't provide direct PDF downloads. "
            "Please use the paper URL to access the publisher's website."
        )
