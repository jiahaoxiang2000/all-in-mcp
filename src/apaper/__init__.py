"""
APaper - Academic Paper Research Module

A specialized module for academic paper search and PDF processing utilities.
Provides tools for searching papers from multiple academic platforms (IACR, 
CryptoBib, Crossref, Google Scholar) and processing PDF documents.
"""

from .models.paper import Paper, read_pdf
from .server import main

__version__ = "0.1.0"
__all__ = ["Paper", "read_pdf", "main"]