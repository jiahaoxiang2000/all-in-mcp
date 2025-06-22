# all_in_mcp/paper.py
import io
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx
from pypdf import PdfReader


@dataclass
class Paper:
    """Standardized paper format with core fields for academic sources"""

    # Core fields (required, but allows empty values or defaults)
    paper_id: str  # Unique identifier (e.g., arXiv ID, PMID, DOI)
    title: str  # Paper title
    authors: list[str]  # List of author names
    abstract: str  # Abstract text
    doi: str  # Digital Object Identifier
    published_date: datetime  # Publication date
    pdf_url: str  # Direct PDF link
    url: str  # URL to paper page
    source: str  # Source platform (e.g., 'arxiv', 'pubmed')

    # Optional fields
    updated_date: datetime | None = None  # Last updated date
    categories: list[str] | None = None  # Subject categories
    keywords: list[str] | None = None  # Keywords
    citations: int = 0  # Citation count
    references: list[str] | None = None  # List of reference IDs/DOIs
    extra: dict | None = None  # Source-specific extra metadata

    def __post_init__(self):
        """Post-initialization to handle default values"""
        if self.authors is None:
            self.authors = []
        if self.categories is None:
            self.categories = []
        if self.keywords is None:
            self.keywords = []
        if self.references is None:
            self.references = []
        if self.extra is None:
            self.extra = {}

    def to_dict(self) -> dict:
        """Convert paper to dictionary format for serialization"""
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "doi": self.doi,
            "published_date": (
                self.published_date.isoformat() if self.published_date else None
            ),
            "pdf_url": self.pdf_url,
            "url": self.url,
            "source": self.source,
            "updated_date": (
                self.updated_date.isoformat() if self.updated_date else None
            ),
            "categories": self.categories,
            "keywords": self.keywords,
            "citations": self.citations,
            "references": self.references,
            "extra": self.extra,
        }

    def read_content(self) -> str:
        """
        Read the full text content of this paper's PDF.

        Returns:
            str: Extracted text content from the paper's PDF

        Raises:
            ValueError: If no PDF URL is available
            Exception: If PDF cannot be read or processed
        """
        if not self.pdf_url:
            raise ValueError("No PDF URL available for this paper")

        return read_pdf(self.pdf_url)


def read_pdf(pdf_source: str | Path) -> str:
    """
    Extract text content from a PDF file (local or online).

    Args:
        pdf_source: Path to local PDF file or URL to online PDF

    Returns:
        str: Extracted text content from the PDF

    Raises:
        FileNotFoundError: If local file doesn't exist
        ValueError: If URL is invalid or PDF cannot be processed
        Exception: For other PDF processing errors
    """
    try:
        if isinstance(pdf_source, str | Path):
            pdf_source_str = str(pdf_source)

            # Check if it's a URL
            parsed = urlparse(pdf_source_str)
            if parsed.scheme in ("http", "https"):
                # Handle online PDF
                return _read_pdf_from_url(pdf_source_str)
            else:
                # Handle local file
                return _read_pdf_from_file(Path(pdf_source_str))
        else:
            raise ValueError("pdf_source must be a string or Path object")

    except Exception as e:
        raise Exception(f"Failed to read PDF from {pdf_source}: {e!s}") from e


def _read_pdf_from_file(file_path: Path) -> str:
    """Read PDF from local file path."""
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if not file_path.suffix.lower() == ".pdf":
        raise ValueError(f"File must have .pdf extension: {file_path}")

    try:
        with open(file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            text_content = []

            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():  # Only add non-empty pages
                        text_content.append(
                            f"--- Page {page_num + 1} ---\n{page_text}\n"
                        )
                except Exception as e:
                    text_content.append(
                        f"--- Page {page_num + 1} (Error reading page: {e!s}) ---\n"
                    )

            return "\n".join(text_content)

    except Exception as e:
        raise Exception(f"Error reading PDF file {file_path}: {e!s}") from e


def _read_pdf_from_url(url: str) -> str:
    """Download and read PDF from URL."""
    try:
        # Download PDF with proper headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        with httpx.Client(timeout=30.0, headers=headers) as client:
            response = client.get(url)
            response.raise_for_status()

            # Check if content is actually a PDF
            content_type = response.headers.get("content-type", "").lower()
            if "application/pdf" not in content_type and not url.lower().endswith(
                ".pdf"
            ):
                # Try to detect PDF by content
                if not response.content.startswith(b"%PDF"):
                    raise ValueError(f"URL does not point to a valid PDF file: {url}")

            # Read PDF from bytes
            pdf_bytes = io.BytesIO(response.content)
            pdf_reader = PdfReader(pdf_bytes)
            text_content = []

            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():  # Only add non-empty pages
                        text_content.append(
                            f"--- Page {page_num + 1} ---\n{page_text}\n"
                        )
                except Exception as e:
                    text_content.append(
                        f"--- Page {page_num + 1} (Error reading page: {e!s}) ---\n"
                    )

            return "\n".join(text_content)

    except httpx.RequestError as e:
        raise Exception(f"Network error downloading PDF from {url}: {e!s}") from e
    except httpx.HTTPStatusError as e:
        raise Exception(
            f"HTTP error {e.response.status_code} downloading PDF from {url}"
        ) from e
    except Exception as e:
        raise Exception(f"Error processing PDF from URL {url}: {e!s}") from e
