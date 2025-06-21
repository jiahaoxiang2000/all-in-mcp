# all_in_mcp/academic_platforms/cryptobib.py
import logging
import os
import random
import re
from datetime import datetime
from pathlib import Path
from typing import ClassVar

import requests

from ..paper import Paper
from .base import PaperSource

logger = logging.getLogger(__name__)


class CryptoBibSearcher(PaperSource):
    """CryptoBib (https://cryptobib.di.ens.fr/) bibliography search implementation"""

    CRYPTOBIB_BASE_URL = "https://cryptobib.di.ens.fr"
    CRYPTOBIB_BIB_URL = "https://cryptobib.di.ens.fr/cryptobib/static/files/crypto.bib"
    BROWSERS: ClassVar[list[str]] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    ]

    def __init__(self, cache_dir: str = "./downloads"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.bib_file_path = self.cache_dir / "crypto.bib"
        self._setup_session()

    def _setup_session(self):
        """Initialize session with random user agent"""
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": random.choice(self.BROWSERS),
                "Accept": "text/plain,text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    def _download_bib_file(self, force_download: bool = False) -> bool:
        """
        Download the crypto.bib file if not exists or if force_download is True

        Args:
            force_download: Force download even if file exists

        Returns:
            bool: True if file is ready, False if download failed
        """
        try:
            # Check if file exists and force_download is False
            if self.bib_file_path.exists() and not force_download:
                logger.info(f"Using cached crypto.bib file at {self.bib_file_path}")
                return True

            logger.info("Downloading crypto.bib file from CryptoBib...")
            response = self.session.get(self.CRYPTOBIB_BIB_URL, stream=True)

            if response.status_code != 200:
                logger.error(
                    f"Failed to download crypto.bib: HTTP {response.status_code}"
                )
                return False

            # Download with progress indication
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(self.bib_file_path, "wb") as f:
                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):  # 1MB chunks
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            if downloaded % (1024 * 1024 * 5) == 0:  # Log every 5MB
                                logger.info(f"Download progress: {progress:.1f}%")

            logger.info(f"Successfully downloaded crypto.bib to {self.bib_file_path}")
            return True

        except requests.RequestException as e:
            logger.error(f"Error downloading crypto.bib: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error downloading crypto.bib: {e}")
            return False

    def _parse_bibtex_entry(self, bibtex_text: str) -> Paper | None:
        """Parse a single BibTeX entry into a Paper object"""
        try:
            # Extract entry type and key
            entry_match = re.match(r"@(\w+){([^,]+),", bibtex_text, re.IGNORECASE)
            if not entry_match:
                return None

            entry_type = entry_match.group(1).lower()
            entry_key = entry_match.group(2).strip()

            # Initialize fields
            title = ""
            authors = []
            year = None
            booktitle = ""
            journal = ""
            pages = ""
            doi = ""
            url = ""
            abstract = ""

            # Extract fields using a more robust approach
            # First, normalize the text by removing extra whitespace
            normalized_text = re.sub(r"\s+", " ", bibtex_text)

            # Extract fields with better pattern matching
            field_dict = {}

            # Pattern for quoted fields (handles multi-line)
            quoted_pattern = r'(\w+)\s*=\s*"([^"]*(?:[^"\\]|\\.)*)"'
            for match in re.finditer(quoted_pattern, bibtex_text, re.DOTALL):
                field_name = match.group(1).lower().strip()
                field_value = match.group(2).strip()
                field_dict[field_name] = field_value

            # Pattern for unquoted fields (like numbers)
            unquoted_pattern = r'(\w+)\s*=\s*([^,}\n"]+)'
            for match in re.finditer(unquoted_pattern, bibtex_text):
                field_name = match.group(1).lower().strip()
                field_value = match.group(2).strip()
                # Only add if not already present from quoted pattern
                if field_name not in field_dict:
                    field_dict[field_name] = field_value

            for field_name, field_value in field_dict.items():
                field_name = field_name.lower().strip()
                field_value = field_value.strip()

                if field_name == "title":
                    # Clean up title (remove LaTeX commands)
                    title = re.sub(r"[{}]", "", field_value)
                    title = re.sub(r"\\[a-zA-Z]+", "", title)
                    title = title.strip()

                elif field_name == "author":
                    # Parse authors - handle "and" separator
                    author_text = re.sub(r"[{}]", "", field_value)
                    authors = [
                        author.strip()
                        for author in re.split(r"\s+and\s+", author_text)
                        if author.strip()
                    ]

                elif field_name == "year":
                    try:
                        year = int(field_value)
                    except ValueError:
                        pass

                elif field_name == "booktitle":
                    booktitle = re.sub(r"[{}]", "", field_value)

                elif field_name == "journal":
                    journal = re.sub(r"[{}]", "", field_value)

                elif field_name == "pages":
                    pages = field_value

                elif field_name == "doi":
                    doi = field_value

                elif field_name == "url":
                    url = field_value

                elif field_name == "abstract":
                    abstract = field_value

            # Determine venue (journal or conference)
            venue = journal if journal else booktitle
            categories = [entry_type] if entry_type else []

            # Create published date
            published_date = datetime(year, 1, 1) if year else datetime(1900, 1, 1)

            return Paper(
                paper_id=entry_key,
                title=title,
                authors=authors,
                abstract=abstract,
                url=url,
                pdf_url="",  # CryptoBib doesn't provide PDF URLs
                published_date=published_date,
                updated_date=None,
                source="cryptobib",
                categories=categories,
                keywords=[],
                doi=doi,
                citations=0,
                extra={
                    "bibtex": bibtex_text.strip(),
                    "venue": venue,
                    "pages": pages,
                    "entry_type": entry_type,
                },
            )

        except Exception as e:
            logger.warning(f"Failed to parse BibTeX entry: {e}")
            return None

    def search_bibtex(
        self,
        query: str,
        max_results: int = 10,
        force_download: bool = False,
        year_min: int | None = None,
        year_max: int | None = None,
    ) -> list[str]:
        """
        Search CryptoBib and return raw BibTeX entries

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            force_download: Force download the newest crypto.bib file
            year_min: Minimum publication year (inclusive, optional)
            year_max: Maximum publication year (inclusive, optional)

        Returns:
            List[str]: List of BibTeX entries as strings

        Example:
            >>> searcher = CryptoBibSearcher()
            >>> # Search for recent implementation papers (2020-2024)
            >>> entries = searcher.search_bibtex("implement", max_results=5,
            ...                                 year_min=2020, year_max=2024)
            >>>
            >>> # Search for older RSA papers (1980-2000)
            >>> entries = searcher.search_bibtex("RSA", max_results=10,
            ...                                 year_min=1980, year_max=2000)
        """
        bibtex_entries = []

        try:
            # Ensure we have the bib file locally
            if not self._download_bib_file(force_download=force_download):
                logger.error("Failed to download crypto.bib file")
                return bibtex_entries

            # Search in the local file
            logger.info(f"Searching local crypto.bib file for: {query}")
            current_entry = ""
            in_entry = False
            brace_count = 0

            # Convert query to lowercase for case-insensitive search
            query_lower = query.lower()

            with open(self.bib_file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    # Check if this is the start of a new entry
                    if line.strip().startswith("@") and not in_entry:
                        current_entry = line
                        in_entry = True
                        brace_count = line.count("{") - line.count("}")
                    elif in_entry:
                        current_entry += line
                        brace_count += line.count("{") - line.count("}")

                        # Check if entry is complete
                        if brace_count <= 0:
                            # Entry is complete, check if it matches the query
                            if query_lower in current_entry.lower():
                                # Check year range if specified
                                if self._entry_matches_year_range(
                                    current_entry, year_min, year_max
                                ):
                                    bibtex_entries.append(current_entry.strip())
                                    logger.info(
                                        f"Found matching entry {len(bibtex_entries)} at line {line_num}"
                                    )

                                    if len(bibtex_entries) >= max_results:
                                        break

                            # Reset for next entry
                            current_entry = ""
                            in_entry = False
                            brace_count = 0

        except FileNotFoundError:
            logger.error(f"crypto.bib file not found at {self.bib_file_path}")
        except Exception as e:
            logger.error(f"CryptoBib search error: {e}")

        return bibtex_entries[:max_results]

    def search(
        self,
        query: str,
        max_results: int = 10,
        return_bibtex: bool = False,
        force_download: bool = False,
        year_min: int | None = None,
        year_max: int | None = None,
    ) -> list[Paper]:
        """
        Search CryptoBib bibliography

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            return_bibtex: If True, include raw BibTeX in results
            force_download: Force download the newest crypto.bib file
            year_min: Minimum publication year (inclusive, optional)
            year_max: Maximum publication year (inclusive, optional)

        Returns:
            List[Paper]: List of paper objects

        Example:
            >>> searcher = CryptoBibSearcher()
            >>> # Search for recent zero-knowledge papers (2020-2024)
            >>> papers = searcher.search("zero knowledge", max_results=5,
            ...                         year_min=2020, year_max=2024)
            >>>
            >>> # Search for classic RSA papers (1977-1990)
            >>> papers = searcher.search("RSA", max_results=10,
            ...                         year_min=1977, year_max=1990)
        """
        papers = []

        try:
            # Get BibTeX entries
            bibtex_entries = self.search_bibtex(
                query,
                max_results,
                force_download=force_download,
                year_min=year_min,
                year_max=year_max,
            )

            # Parse each entry into Paper objects
            for i, bibtex_text in enumerate(bibtex_entries):
                logger.info(f"Parsing entry {i+1}/{len(bibtex_entries)}")
                paper = self._parse_bibtex_entry(bibtex_text)
                if paper:
                    papers.append(paper)

        except Exception as e:
            logger.error(f"CryptoBib search error: {e}")

        return papers

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        """
        CryptoBib doesn't provide PDF downloads
        """
        return "Error: CryptoBib is a bibliography database and doesn't provide PDF downloads"

    def read_paper(self, paper_id: str, save_path: str = "./downloads") -> str:
        """
        CryptoBib doesn't provide paper content reading
        """
        return "Error: CryptoBib is a bibliography database and doesn't provide paper content"

    def get_bibtex_by_key(
        self, entry_key: str, force_download: bool = False
    ) -> str | None:
        """
        Get a specific BibTeX entry by its key

        Args:
            entry_key: The BibTeX entry key (e.g., "ACISP:LZXSW24")
            force_download: Force download the newest crypto.bib file

        Returns:
            str: The BibTeX entry or None if not found
        """
        try:
            # Ensure we have the bib file locally
            if not self._download_bib_file(force_download=force_download):
                logger.error("Failed to download crypto.bib file")
                return None

            logger.info(f"Searching for BibTeX entry: {entry_key}")
            current_entry = ""
            in_entry = False
            brace_count = 0

            with open(self.bib_file_path, "r", encoding="utf-8") as f:
                for line in f:
                    # Check if this is the start of the entry we're looking for
                    if line.strip().startswith(f"@") and entry_key in line:
                        current_entry = line
                        in_entry = True
                        brace_count = line.count("{") - line.count("}")
                    elif in_entry:
                        current_entry += line
                        brace_count += line.count("{") - line.count("}")

                        # Check if entry is complete
                        if brace_count <= 0:
                            return current_entry.strip()

        except FileNotFoundError:
            logger.error(f"crypto.bib file not found at {self.bib_file_path}")
        except Exception as e:
            logger.error(f"Error searching for entry {entry_key}: {e}")

        return None

    def _entry_matches_year_range(
        self, bibtex_entry: str, year_min: int | None, year_max: int | None
    ) -> bool:
        """
        Check if a BibTeX entry falls within the specified year range

        Args:
            bibtex_entry: Raw BibTeX entry text
            year_min: Minimum year (inclusive, None means no minimum)
            year_max: Maximum year (inclusive, None means no maximum)

        Returns:
            bool: True if entry is within year range, False otherwise
        """
        # If no year constraints specified, all entries match
        if year_min is None and year_max is None:
            return True

        try:
            # Extract year from the BibTeX entry
            year_match = re.search(
                r'year\s*=\s*(?:["{\s]*)?(\d{4})', bibtex_entry, re.IGNORECASE
            )
            if not year_match:
                # If no year found, exclude from results when year filtering is requested
                return False

            entry_year = int(year_match.group(1))

            # Check minimum year constraint
            if year_min is not None and entry_year < year_min:
                return False

            # Check maximum year constraint
            if year_max is not None and entry_year > year_max:
                return False

            return True

        except (ValueError, AttributeError):
            # If year parsing fails, exclude from results when year filtering is requested
            return False
