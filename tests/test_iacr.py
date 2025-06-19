# tests/test_iacr.py
"""
Unit tests for IACR paper search functionality
"""
import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from all_in_mcp.academic_platforms.iacr import IACRSearcher


class TestIACRSearcher(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.searcher = IACRSearcher()

    def test_search_basic(self):
        """Test basic search functionality"""
        papers = self.searcher.search("cryptography", max_results=5)
        self.assertIsInstance(papers, list)
        self.assertLessEqual(len(papers), 5)

        if papers:
            paper = papers[0]
            self.assertIsNotNone(paper.title)
            self.assertIsNotNone(paper.paper_id)
            self.assertIsNotNone(paper.authors)
            self.assertEqual(paper.source, "iacr")

    def test_search_empty_query(self):
        """Test search with empty query"""
        papers = self.searcher.search("", max_results=5)
        self.assertIsInstance(papers, list)

    def test_search_max_results(self):
        """Test search respects max_results parameter"""
        papers = self.searcher.search("zero knowledge", max_results=3)
        self.assertLessEqual(len(papers), 3)

    def test_download_pdf_invalid_id(self):
        """Test download with invalid paper ID"""
        try:
            result = self.searcher.download_pdf("invalid/id", "./downloads")
            # If no exception, check if it's an error message
            self.assertIsInstance(result, str)
            # Could be empty string or error message for invalid ID
        except Exception:
            # Exception is expected for invalid ID
            pass

    def test_read_paper_nonexistent(self):
        """Test reading non-existent paper"""
        result = self.searcher.read_paper("nonexistent/paper", "./downloads")
        self.assertIsInstance(result, str)
        # Should return empty string or error message for non-existent paper

    def test_get_paper_details_valid_id(self):
        """Test getting paper details with a valid paper ID"""
        # Use a recent paper ID that's likely to exist
        # Note: In real tests, you might want to use a known stable paper ID
        papers = self.searcher.search("cryptography", max_results=1)
        if papers:
            paper_id = papers[0].paper_id
            detailed_paper = self.searcher.get_paper_details(paper_id)

            self.assertIsNotNone(detailed_paper)
            if detailed_paper:
                self.assertEqual(detailed_paper.paper_id, paper_id)
                self.assertIsNotNone(detailed_paper.title)
                self.assertIsNotNone(detailed_paper.authors)
                self.assertEqual(detailed_paper.source, "iacr")
                self.assertIsNotNone(detailed_paper.url)
                self.assertIsNotNone(detailed_paper.pdf_url)

                # Check that PDF URL follows IACR format
                expected_pdf_url = f"https://eprint.iacr.org/{paper_id}.pdf"
                self.assertEqual(detailed_paper.pdf_url, expected_pdf_url)

    def test_get_paper_details_invalid_id(self):
        """Test getting paper details with an invalid paper ID"""
        detailed_paper = self.searcher.get_paper_details("9999/9999")
        self.assertIsNone(detailed_paper)

    def test_get_paper_details_with_url(self):
        """Test getting paper details using a full URL instead of just paper ID"""
        # Get a valid paper first
        papers = self.searcher.search("zero knowledge", max_results=1)
        if papers:
            paper_url = papers[0].url
            detailed_paper = self.searcher.get_paper_details(paper_url)

            self.assertIsNotNone(detailed_paper)
            if detailed_paper:
                self.assertEqual(detailed_paper.url, paper_url)
                self.assertEqual(detailed_paper.source, "iacr")


if __name__ == "__main__":
    unittest.main()
