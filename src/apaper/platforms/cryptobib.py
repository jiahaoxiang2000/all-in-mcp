# apaper/platforms/cryptobib.py
import logging
import random
import re
from datetime import datetime
from pathlib import Path
from typing import ClassVar

import requests

from ..models.paper import Paper
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
        """Download the crypto.bib file if not exists or if force_download is True"""
        try:
            if self.bib_file_path.exists() and not force_download:
                logger.info(f"Using cached crypto.bib file at {self.bib_file_path}")
                return True

            logger.info("Downloading crypto.bib file from CryptoBib...")
            response = self.session.get(self.CRYPTOBIB_BIB_URL, stream=True)

            if response.status_code != 200:
                logger.error(f"Failed to download crypto.bib: HTTP {response.status_code}")
                return False

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(self.bib_file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            if downloaded % (1024 * 1024 * 5) == 0:
                                logger.info(f"Download progress: {progress:.1f}%")

            logger.info(f"Successfully downloaded crypto.bib to {self.bib_file_path}")
            return True

        except Exception as e:
            logger.error(f"Error downloading crypto.bib: {e}")
            return False

    def _parse_bibtex_entry(self, bibtex_text: str) -> Paper | None:
        """Parse a single BibTeX entry into a Paper object"""
        try:
            entry_match = re.match(r"@(\w+){([^,]+),", bibtex_text, re.IGNORECASE)
            if not entry_match:
                return None

            entry_type = entry_match.group(1).lower()
            entry_key = entry_match.group(2).strip()

            # Extract fields using regex patterns
            field_dict = {}
            
            # Pattern for quoted fields
            quoted_pattern = r'(\w+)\s*=\s*"([^"]*(?:[^"\\]|\\.)*)"'
            for match in re.finditer(quoted_pattern, bibtex_text, re.DOTALL):
                field_name = match.group(1).lower().strip()
                field_value = match.group(2).strip()
                field_dict[field_name] = field_value

            # Pattern for unquoted fields
            unquoted_pattern = r'(\w+)\s*=\s*([^,}\n"]+)'
            for match in re.finditer(unquoted_pattern, bibtex_text):
                field_name = match.group(1).lower().strip()
                field_value = match.group(2).strip()
                if field_name not in field_dict:
                    field_dict[field_name] = field_value

            # Parse fields
            title = re.sub(r"[{}]", "", field_dict.get("title", "")).strip()
            title = re.sub(r"\\[a-zA-Z]+", "", title).strip()
            
            authors = []
            if "author" in field_dict:
                author_text = re.sub(r"[{}]", "", field_dict["author"])
                authors = [author.strip() for author in re.split(r"\s+and\s+", author_text) if author.strip()]
            
            year = None
            if "year" in field_dict:
                try:
                    year = int(field_dict["year"])
                except ValueError:
                    pass

            venue = field_dict.get("journal") or field_dict.get("booktitle", "")
            venue = re.sub(r"[{}]", "", venue)

            published_date = datetime(year, 1, 1) if year else datetime(1900, 1, 1)

            return Paper(
                paper_id=entry_key,
                title=title,
                authors=authors,
                abstract=field_dict.get("abstract", ""),
                url=field_dict.get("url", ""),
                pdf_url="",  # CryptoBib doesn't provide PDF URLs
                published_date=published_date,
                updated_date=None,
                source="cryptobib",
                categories=[entry_type] if entry_type else [],
                keywords=[],
                doi=field_dict.get("doi", ""),
                citations=0,
                extra={
                    "bibtex": bibtex_text.strip(),
                    "venue": venue,
                    "pages": field_dict.get("pages", ""),
                    "entry_type": entry_type,
                },
            )

        except Exception as e:
            logger.warning(f"Failed to parse BibTeX entry: {e}")
            return None

    def search_bibtex(self, query: str, max_results: int = 10, force_download: bool = False, 
                     year_min: int | None = None, year_max: int | None = None) -> list[str]:
        """Search CryptoBib and return raw BibTeX entries"""
        bibtex_entries = []

        try:
            if not self._download_bib_file(force_download=force_download):
                logger.error("Failed to download crypto.bib file")
                return bibtex_entries

            logger.info(f"Searching local crypto.bib file for: {query}")
            current_entry = ""
            in_entry = False
            brace_count = 0
            query_lower = query.lower()

            with open(self.bib_file_path, encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip().startswith("@") and not in_entry:
                        current_entry = line
                        in_entry = True
                        brace_count = line.count("{") - line.count("}")
                    elif in_entry:
                        current_entry += line
                        brace_count += line.count("{") - line.count("}")

                        if brace_count <= 0:
                            if query_lower in current_entry.lower():
                                if self._entry_matches_year_range(current_entry, year_min, year_max):
                                    bibtex_entries.append(current_entry.strip())
                                    if len(bibtex_entries) >= max_results:
                                        break

                            current_entry = ""
                            in_entry = False
                            brace_count = 0

        except Exception as e:
            logger.error(f"CryptoBib search error: {e}")

        return bibtex_entries[:max_results]

    def search(self, query: str, max_results: int = 10, return_bibtex: bool = False,
               force_download: bool = False, year_min: int | None = None, 
               year_max: int | None = None) -> list[Paper]:
        """Search CryptoBib bibliography"""
        papers = []
        try:
            bibtex_entries = self.search_bibtex(query, max_results, force_download=force_download,
                                              year_min=year_min, year_max=year_max)
            for bibtex_text in bibtex_entries:
                paper = self._parse_bibtex_entry(bibtex_text)
                if paper:
                    papers.append(paper)
        except Exception as e:
            logger.error(f"CryptoBib search error: {e}")
        return papers

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        """CryptoBib doesn't provide PDF downloads"""
        return "Error: CryptoBib is a bibliography database and doesn't provide PDF downloads"

    def read_paper(self, paper_id: str, save_path: str = "./downloads", 
                  start_page: int | None = None, end_page: int | None = None) -> str:
        """CryptoBib doesn't provide paper content reading"""
        return "Error: CryptoBib is a bibliography database and doesn't provide paper content"

    def _entry_matches_year_range(self, bibtex_entry: str, year_min: int | None, 
                                 year_max: int | None) -> bool:
        """Check if a BibTeX entry falls within the specified year range"""
        if year_min is None and year_max is None:
            return True

        try:
            year_match = re.search(r'year\s*=\s*(?:["{\s]*)?(\d{4})', bibtex_entry, re.IGNORECASE)
            if not year_match:
                return False

            entry_year = int(year_match.group(1))
            
            if year_min is not None and entry_year < year_min:
                return False
            if year_max is not None and entry_year > year_max:
                return False
            
            return True

        except (ValueError, AttributeError):
            return False