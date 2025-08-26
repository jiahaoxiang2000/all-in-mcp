# apaper/utils/pdf_reader.py
import io
from pathlib import Path
from urllib.parse import urlparse

import httpx
from pypdf import PdfReader


def read_pdf(pdf_source: str | Path, start_page: int | None = None, end_page: int | None = None) -> str:
    """
    Extract text content from a PDF file (local or online).

    Args:
        pdf_source: Path to local PDF file or URL to online PDF
        start_page: Starting page number (1-indexed, inclusive). Defaults to 1.
        end_page: Ending page number (1-indexed, inclusive). Defaults to last page.

    Returns:
        str: Extracted text content from the PDF

    Raises:
        FileNotFoundError: If local file doesn't exist
        ValueError: If URL is invalid, PDF cannot be processed, or page range is invalid
        Exception: For other PDF processing errors
    """
    try:
        if isinstance(pdf_source, str | Path):
            pdf_source_str = str(pdf_source)

            # Check if it's a URL
            parsed = urlparse(pdf_source_str)
            if parsed.scheme in ("http", "https"):
                # Handle online PDF
                return _read_pdf_from_url(pdf_source_str, start_page, end_page)
            else:
                # Handle local file
                return _read_pdf_from_file(Path(pdf_source_str), start_page, end_page)
        else:
            raise ValueError("pdf_source must be a string or Path object")

    except Exception as e:
        raise Exception(f"Failed to read PDF from {pdf_source}: {e!s}") from e


def _normalize_page_range(start_page: int | None, end_page: int | None, total_pages: int) -> tuple[int, int]:
    """
    Normalize and validate page range parameters.
    
    Args:
        start_page: Starting page number (1-indexed, inclusive) or None
        end_page: Ending page number (1-indexed, inclusive) or None
        total_pages: Total number of pages in the PDF
        
    Returns:
        tuple[int, int]: (start_index, end_index) as 0-indexed values
        
    Raises:
        ValueError: If page range is invalid
    """
    # Default values
    if start_page is None:
        start_page = 1
    if end_page is None:
        end_page = total_pages
        
    # Validate page numbers
    if start_page < 1:
        raise ValueError(f"start_page must be >= 1, got {start_page}")
    if end_page < 1:
        raise ValueError(f"end_page must be >= 1, got {end_page}")
    if start_page > end_page:
        raise ValueError(f"start_page ({start_page}) must be <= end_page ({end_page})")
    if start_page > total_pages:
        raise ValueError(f"start_page ({start_page}) exceeds total pages ({total_pages})")
        
    # Clamp end_page to total_pages
    if end_page > total_pages:
        end_page = total_pages
        
    # Convert to 0-indexed
    return start_page - 1, end_page - 1


def _read_pdf_from_file(file_path: Path, start_page: int | None = None, end_page: int | None = None) -> str:
    """Read PDF from local file path."""
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if not file_path.suffix.lower() == ".pdf":
        raise ValueError(f"File must have .pdf extension: {file_path}")

    try:
        with open(file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            # Validate and normalize page range
            start_idx, end_idx = _normalize_page_range(start_page, end_page, total_pages)
            
            text_content = []

            for page_num in range(start_idx, end_idx + 1):
                try:
                    page = pdf_reader.pages[page_num]
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


def _read_pdf_from_url(url: str, start_page: int | None = None, end_page: int | None = None) -> str:
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
            total_pages = len(pdf_reader.pages)
            
            # Validate and normalize page range
            start_idx, end_idx = _normalize_page_range(start_page, end_page, total_pages)
            
            text_content = []

            for page_num in range(start_idx, end_idx + 1):
                try:
                    page = pdf_reader.pages[page_num]
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