# apaper/models/paper.py
from dataclasses import dataclass
from datetime import datetime


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
