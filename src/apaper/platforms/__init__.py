"""APaper academic platforms module."""

from .base import PaperSource
from .iacr import IACRSearcher
from .dblp import DBLPSearcher
from .google_scholar import GoogleScholarSearcher

__all__ = [
    "PaperSource",
    "IACRSearcher",
    "DBLPSearcher",
    "GoogleScholarSearcher",
]
