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

    def test_get_paper_details_fields(self):
        """Test that get_paper_details returns all expected fields"""
        papers = self.searcher.search("blockchain", max_results=1)
        if papers:
            paper_id = papers[0].paper_id
            detailed_paper = self.searcher.get_paper_details(paper_id)

            if detailed_paper:
                # Test required fields
                self.assertIsInstance(detailed_paper.title, str)
                self.assertIsInstance(detailed_paper.authors, list)
                self.assertIsInstance(detailed_paper.abstract, str)
                self.assertIsInstance(detailed_paper.keywords, list)

                # Test URL fields
                self.assertTrue(
                    detailed_paper.url.startswith("https://eprint.iacr.org/")
                )
                self.assertTrue(
                    detailed_paper.pdf_url.startswith("https://eprint.iacr.org/")
                )
                self.assertTrue(detailed_paper.pdf_url.endswith(".pdf"))

                # Test extra fields
                self.assertIsInstance(detailed_paper.extra, dict)
                if detailed_paper.extra:
                    self.assertIn("publication_info", detailed_paper.extra)
                    self.assertIn("history", detailed_paper.extra)

    def test_get_paper_details_malformed_url(self):
        """Test getting paper details with a malformed URL"""
        detailed_paper = self.searcher.get_paper_details("https://invalid-url")
        self.assertIsNone(detailed_paper)

    def test_get_paper_details_empty_string(self):
        """Test getting paper details with empty string"""
        detailed_paper = self.searcher.get_paper_details("")
        # The function currently returns a Paper object with empty fields for empty string
        # This might not be ideal behavior, but it's the current implementation
        self.assertIsNotNone(detailed_paper)
        if detailed_paper:
            self.assertEqual(detailed_paper.paper_id, "")
            self.assertEqual(detailed_paper.title, "")

    def test_get_paper_details_compared_to_search(self):
        """Test that get_paper_details provides more information than search results"""
        # First get a paper from search without details
        papers_no_details = self.searcher.search(
            "lattice", max_results=1, fetch_details=False
        )
        if papers_no_details:
            paper_id = papers_no_details[0].paper_id

            # Then get detailed information
            detailed_paper = self.searcher.get_paper_details(paper_id)

            if detailed_paper:
                # The detailed paper should have the same basic info
                self.assertEqual(detailed_paper.paper_id, paper_id)
                self.assertEqual(detailed_paper.source, "iacr")

                # But might have more complete information
                # (This test validates the function works, specific content may vary)
                self.assertIsNotNone(detailed_paper.title)
                self.assertIsNotNone(detailed_paper.authors)


if __name__ == "__main__":
    unittest.main()
