# all_in_mcp/academic_platforms/base.py
from abc import ABC, abstractmethod

from ..paper import Paper


class PaperSource(ABC):
    """Abstract base class for paper sources"""

    @abstractmethod
    def search(self, query: str, **kwargs) -> list[Paper]:
        """Search for papers based on query"""
        raise NotImplementedError

    @abstractmethod
    def download_pdf(self, paper_id: str, save_path: str) -> str:
        """Download PDF of a paper"""
        raise NotImplementedError

    @abstractmethod
    def read_paper(self, paper_id: str, save_path: str) -> str:
        """Read and extract text content from a paper"""
        raise NotImplementedError
