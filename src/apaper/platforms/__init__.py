"""APaper academic platforms module."""

from .base import PaperSource
from .iacr import IACRSearcher
from .cryptobib import CryptoBibSearcher
from .crossref import CrossrefSearcher
from .google_scholar import GoogleScholarSearcher

__all__ = [
    "PaperSource",
    "IACRSearcher", 
    "CryptoBibSearcher",
    "CrossrefSearcher",
    "GoogleScholarSearcher"
]