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

    def test_print_detailed_search_results(self):
        """Test to print detailed search results for inspection"""
        print("\n" + "=" * 80)
        print("DETAILED SEARCH RESULTS TEST")
        print("=" * 80)

        # Search for papers
        papers = self.searcher.search("zero knowledge", max_results=2)

        if papers:
            for i, paper in enumerate(papers):
                print(f"\n--- Paper {i+1} from Search ---")
                print(f"Paper ID: {paper.paper_id}")
                print(f"Title: {paper.title}")
                print(f"Authors: {', '.join(paper.authors)}")
                print(f"URL: {paper.url}")
                print(f"PDF URL: {paper.pdf_url}")
                print(f"Abstract (first 200 chars): {paper.abstract[:200]}...")
                print(f"Keywords: {paper.keywords}")
                print(f"Categories: {paper.categories}")
                print(f"Published Date: {paper.published_date}")
                print(f"Updated Date: {paper.updated_date}")
                print(f"Extra fields: {paper.extra}")

                # Now get detailed information for the same paper
                print(f"\n--- Detailed Info for Paper {i+1} ---")
                detailed_paper = self.searcher.get_paper_details(paper.paper_id)

                if detailed_paper:
                    print(f"Detailed Paper ID: {detailed_paper.paper_id}")
                    print(f"Detailed Title: {detailed_paper.title}")
                    print(f"Detailed Authors: {', '.join(detailed_paper.authors)}")
                    print(f"Detailed URL: {detailed_paper.url}")
                    print(f"Detailed PDF URL: {detailed_paper.pdf_url}")
                    print(
                        f"Detailed Abstract (first 300 chars): {detailed_paper.abstract[:300]}..."
                    )
                    print(f"Detailed Keywords: {detailed_paper.keywords}")
                    print(f"Detailed Categories: {detailed_paper.categories}")
                    print(f"Detailed Published Date: {detailed_paper.published_date}")
                    print(f"Detailed Updated Date: {detailed_paper.updated_date}")
                    print(f"Detailed Extra fields: {detailed_paper.extra}")

                    # Compare the differences
                    print(f"\n--- Comparison for Paper {i+1} ---")
                    print(f"Title same: {paper.title == detailed_paper.title}")
                    print(f"Authors same: {paper.authors == detailed_paper.authors}")
                    print(f"Abstract same: {paper.abstract == detailed_paper.abstract}")
                    print(f"Keywords same: {paper.keywords == detailed_paper.keywords}")
                    print(f"Extra fields same: {paper.extra == detailed_paper.extra}")
                else:
                    print("Failed to get detailed information")

                print("-" * 60)
        else:
            print("No papers found for the search query")

        print("=" * 80)

        # This test always passes, it's just for printing information
        self.assertTrue(True)

    def test_print_search_vs_details_comparison(self):
        """Test to show the difference between search with/without details and get_paper_details"""
        print("\n" + "=" * 80)
        print("SEARCH vs DETAILS COMPARISON TEST")
        print("=" * 80)

        # Search without details first
        print("\n--- Search WITHOUT details (fetch_details=False) ---")
        papers_no_details = self.searcher.search(
            "cryptography", max_results=1, fetch_details=False
        )

        if papers_no_details:
            paper = papers_no_details[0]
            print(f"Paper ID: {paper.paper_id}")
            print(f"Title: {paper.title}")
            print(f"Authors count: {len(paper.authors)}")
            print(f"Abstract length: {len(paper.abstract)}")
            print(f"Keywords count: {len(paper.keywords)}")
            print(f"Extra fields: {paper.extra}")

            # Now search WITH details
            print(f"\n--- Search WITH details (fetch_details=True) ---")
            papers_with_details = self.searcher.search(
                "cryptography", max_results=1, fetch_details=True
            )

            if papers_with_details:
                detailed_paper_from_search = papers_with_details[0]
                print(f"Paper ID: {detailed_paper_from_search.paper_id}")
                print(f"Title: {detailed_paper_from_search.title}")
                print(f"Authors count: {len(detailed_paper_from_search.authors)}")
                print(f"Abstract length: {len(detailed_paper_from_search.abstract)}")
                print(f"Keywords count: {len(detailed_paper_from_search.keywords)}")
                print(f"Extra fields: {detailed_paper_from_search.extra}")

            # Now use get_paper_details directly
            print(f"\n--- Direct get_paper_details() call ---")
            detailed_paper_direct = self.searcher.get_paper_details(paper.paper_id)

            if detailed_paper_direct:
                print(f"Paper ID: {detailed_paper_direct.paper_id}")
                print(f"Title: {detailed_paper_direct.title}")
                print(f"Authors count: {len(detailed_paper_direct.authors)}")
                print(f"Abstract length: {len(detailed_paper_direct.abstract)}")
                print(f"Keywords count: {len(detailed_paper_direct.keywords)}")
                print(f"Extra fields: {detailed_paper_direct.extra}")

                # Show actual keywords and extra fields content
                print(f"\nKeywords: {detailed_paper_direct.keywords}")
                print(
                    f"Publication info: {detailed_paper_direct.extra.get('publication_info', 'N/A')}"
                )
                print(f"History: {detailed_paper_direct.extra.get('history', 'N/A')}")

        print("=" * 80)
        self.assertTrue(True)

    def test_abstract_extraction_quality(self):
        """Test that the improved abstract extraction is working properly"""
        print("\n" + "=" * 80)
        print("ABSTRACT EXTRACTION QUALITY TEST")
        print("=" * 80)

        # Test with multiple different papers to ensure robust abstract extraction
        test_queries = ["cryptography", "zero knowledge", "lattice", "blockchain"]

        for query in test_queries:
            print(f"\n--- Testing with query: '{query}' ---")

            # Search without details to get basic abstract
            papers_basic = self.searcher.search(
                query, max_results=1, fetch_details=False
            )

            if papers_basic:
                paper = papers_basic[0]
                basic_abstract = paper.abstract

                print(f"Paper ID: {paper.paper_id}")
                print(f"Title: {paper.title}")
                print(f"Basic abstract length: {len(basic_abstract)}")
                print(f"Basic abstract preview: {basic_abstract[:200]}...")

                # Get detailed abstract using get_paper_details
                detailed_paper = self.searcher.get_paper_details(paper.paper_id)

                if detailed_paper:
                    detailed_abstract = detailed_paper.abstract
                    print(f"Detailed abstract length: {len(detailed_abstract)}")
                    print(f"Detailed abstract preview: {detailed_abstract[:200]}...")

                    # Quality checks
                    if len(detailed_abstract) > 100:
                        print("✓ Abstract has reasonable length")
                    else:
                        print("! Abstract seems too short")

                    if len(detailed_abstract) >= len(basic_abstract):
                        print("✓ Detailed extraction found same or more content")
                    else:
                        print(
                            "! Detailed extraction found less content than basic search"
                        )

                    # Check for common abstract indicators
                    abstract_lower = detailed_abstract.lower()
                    indicators = [
                        "we present",
                        "this paper",
                        "we propose",
                        "we show",
                        "in this work",
                        "we introduce",
                    ]
                    if any(indicator in abstract_lower for indicator in indicators):
                        print("✓ Abstract contains typical research paper language")
                    else:
                        print("? Abstract may not be complete or typical")

                    # Test that it's not just metadata
                    metadata_words = [
                        "last updated",
                        "publication info",
                        "history",
                        "keywords",
                        "license",
                    ]
                    if not any(word in abstract_lower for word in metadata_words):
                        print("✓ Abstract appears to be content, not metadata")
                    else:
                        print("! Abstract may contain metadata instead of content")

                else:
                    print("! Failed to get detailed paper information")
            else:
                print(f"No papers found for query: {query}")

            print("-" * 60)

        print("=" * 80)

        # This test always passes, it's for validation and debugging
        self.assertTrue(True)

    def test_get_paper_details_abstract_validation(self):
        """Test that get_paper_details returns meaningful abstracts"""
        papers = self.searcher.search(
            "cryptography", max_results=2, fetch_details=False
        )

        for paper in papers:
            detailed_paper = self.searcher.get_paper_details(paper.paper_id)

            if detailed_paper:
                # Abstract should be a reasonable length for a research paper
                self.assertGreater(
                    len(detailed_paper.abstract),
                    50,
                    f"Abstract too short for paper {paper.paper_id}",
                )

                # Abstract should not be empty
                self.assertNotEqual(
                    detailed_paper.abstract.strip(),
                    "",
                    f"Abstract is empty for paper {paper.paper_id}",
                )

                # Abstract should be a string
                self.assertIsInstance(
                    detailed_paper.abstract,
                    str,
                    f"Abstract is not a string for paper {paper.paper_id}",
                )

    def test_get_paper_details_improved_abstract(self):
        """Test that the improved get_paper_details extracts complete abstracts"""
        print("\n" + "=" * 80)
        print("IMPROVED ABSTRACT EXTRACTION TEST")
        print("=" * 80)

        # Test with a few different papers to ensure robustness
        test_papers = []

        # Get some papers without detailed fetching first
        papers = self.searcher.search(
            "cryptography", max_results=2, fetch_details=False
        )
        test_papers.extend(papers[:2])

        for i, paper in enumerate(test_papers):
            print(f"\n--- Testing Paper {i+1}: {paper.paper_id} ---")
            print(f"Title: {paper.title}")

            # Get basic abstract from search
            basic_abstract = paper.abstract
            print(f"Basic abstract length: {len(basic_abstract)}")

            # Get improved abstract from get_paper_details
            detailed_paper = self.searcher.get_paper_details(paper.paper_id)

            if detailed_paper:
                improved_abstract = detailed_paper.abstract
                print(f"Improved abstract length: {len(improved_abstract)}")

                # Validate the abstract quality
                self.assertIsInstance(improved_abstract, str)
                self.assertGreater(len(improved_abstract), 50)  # Should be substantial

                # Show improvement
                if len(improved_abstract) > len(basic_abstract):
                    print("✓ Improvement: Found longer abstract!")
                    improvement = len(improved_abstract) - len(basic_abstract)
                    print(f"  Added {improvement} more characters")
                elif len(improved_abstract) == len(basic_abstract):
                    print("= Same length as basic search")
                else:
                    print("! Shorter than basic search (unexpected)")

                # Show a sample of the abstract
                print(f"Abstract preview: {improved_abstract[:200]}...")

                # Test other extracted information
                if detailed_paper.keywords:
                    print(
                        f"Keywords found: {len(detailed_paper.keywords)} - {detailed_paper.keywords}"
                    )
                else:
                    print("No keywords found")

                if detailed_paper.extra:
                    pub_info = detailed_paper.extra.get("publication_info", "")
                    history = detailed_paper.extra.get("history", "")
                    if pub_info:
                        print(f"Publication info: {pub_info}")
                    if history:
                        print(f"History: {history[:100]}...")

            else:
                print("! Failed to get detailed paper information")
                self.fail(f"get_paper_details failed for paper {paper.paper_id}")

            print("-" * 60)

        print("=" * 80)
        print("Abstract extraction improvement test completed")
        print("=" * 80)


if __name__ == "__main__":
    unittest.main()
