# tests/test_apaper_iacr.py
"""
Unit tests for APaper IACR functionality
"""
import unittest
import sys
import os

# Add the src directory to the path so we can import our modules  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from apaper.platforms.iacr import IACRSearcher
from apaper.models.paper import Paper


class TestAPaperIACRSearcher(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.searcher = IACRSearcher()
    
    def test_search_basic(self):
        """Test basic search functionality"""
        papers = self.searcher.search("cryptography", max_results=3, fetch_details=False)
        self.assertIsInstance(papers, list)
        self.assertLessEqual(len(papers), 3)
        
        if papers:
            paper = papers[0]
            self.assertIsInstance(paper, Paper)
            self.assertIsNotNone(paper.title)
            self.assertIsNotNone(paper.paper_id)
            self.assertIsInstance(paper.authors, list)
            self.assertEqual(paper.source, "iacr")
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        papers = self.searcher.search("", max_results=2, fetch_details=False)
        self.assertIsInstance(papers, list)
    
    def test_search_max_results(self):
        """Test search respects max_results parameter"""
        papers = self.searcher.search("zero knowledge", max_results=2, fetch_details=False)
        self.assertLessEqual(len(papers), 2)
    
    def test_paper_model(self):
        """Test Paper model functionality"""
        from datetime import datetime
        
        paper = Paper(
            paper_id="test/123",
            title="Test Paper",
            authors=["Author One", "Author Two"],
            abstract="This is a test abstract",
            doi="",
            published_date=datetime.now(),
            pdf_url="https://example.com/test.pdf",
            url="https://example.com/paper",
            source="iacr"
        )
        
        self.assertEqual(paper.paper_id, "test/123")
        self.assertEqual(paper.title, "Test Paper")
        self.assertEqual(len(paper.authors), 2)
        self.assertEqual(paper.source, "iacr")
        
        # Test to_dict method
        paper_dict = paper.to_dict()
        self.assertIsInstance(paper_dict, dict)
        self.assertEqual(paper_dict["paper_id"], "test/123")
        self.assertEqual(paper_dict["title"], "Test Paper")


if __name__ == "__main__":
    unittest.main()