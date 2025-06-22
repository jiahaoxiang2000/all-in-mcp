# tests/test_google_scholar.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from all_in_mcp.academic_platforms.google_scholar import GoogleScholarSearcher
from all_in_mcp.paper import Paper


class TestGoogleScholarSearcher:
    """Test cases for Google Scholar searcher"""

    def setup_method(self):
        """Set up test fixtures"""
        self.searcher = GoogleScholarSearcher()

    def test_init(self):
        """Test searcher initialization"""
        assert self.searcher is not None
        assert hasattr(self.searcher, "session")
        assert "User-Agent" in self.searcher.session.headers

    def test_extract_year(self):
        """Test year extraction from text"""
        test_cases = [
            ("Published in 2023", 2023),
            ("Conference 2020 - ACM", 2020),
            ("Some text 1999 more text", 1999),
            ("No year here", None),
            ("Invalid year 1850", None),  # Too old
            ("Future year 2050", None),  # Too new
        ]

        for text, expected in test_cases:
            result = self.searcher._extract_year(text)
            assert result == expected, f"Failed for text: {text}"

    def test_extract_citations(self):
        """Test citation count extraction"""
        # Mock HTML element with citation info
        mock_item = Mock()
        mock_citation_elem = Mock()
        mock_citation_link = Mock()

        # Test case with citations
        mock_citation_link.get_text.return_value = "Cited by 42"
        mock_citation_elem.find.return_value = mock_citation_link
        mock_item.find.return_value = mock_citation_elem

        result = self.searcher._extract_citations(mock_item)
        assert result == 42

        # Test case with no citations
        mock_item.find.return_value = None
        result = self.searcher._extract_citations(mock_item)
        assert result == 0

    @patch("all_in_mcp.academic_platforms.google_scholar.requests.Session.get")
    def test_search_success(self, mock_get):
        """Test successful search"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <div class="gs_ri">
                <h3 class="gs_rt">
                    <a href="http://example.com/paper1">Test Paper Title</a>
                </h3>
                <div class="gs_a">Author Name - Conference 2023</div>
                <div class="gs_rs">This is the abstract of the paper.</div>
                <div class="gs_fl">
                    <a>Cited by 10</a>
                </div>
            </div>
        </html>
        """
        mock_get.return_value = mock_response

        # Test search
        with patch("time.sleep"):  # Skip sleep delays in tests
            results = self.searcher.search("test query", max_results=1)

        assert len(results) == 1
        paper = results[0]
        assert isinstance(paper, Paper)
        assert paper.title == "Test Paper Title"
        assert paper.source == "google_scholar"
        assert paper.url == "http://example.com/paper1"

    @patch("all_in_mcp.academic_platforms.google_scholar.requests.Session.get")
    def test_search_empty_results(self, mock_get):
        """Test search with no results"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><div>No results</div></html>"
        mock_get.return_value = mock_response

        with patch("time.sleep"):
            results = self.searcher.search("nonexistent query")

        assert len(results) == 0

    @patch("all_in_mcp.academic_platforms.google_scholar.requests.Session.get")
    def test_search_http_error(self, mock_get):
        """Test search with HTTP error"""
        mock_response = Mock()
        mock_response.status_code = 429  # Rate limited
        mock_get.return_value = mock_response

        with patch("time.sleep"):
            results = self.searcher.search("test query")

        assert len(results) == 0

    def test_download_pdf_not_implemented(self):
        """Test that PDF download raises NotImplementedError"""
        with pytest.raises(NotImplementedError) as exc_info:
            self.searcher.download_pdf("some_id", "./downloads")

        assert "doesn't provide direct PDF downloads" in str(exc_info.value)

    def test_read_paper_not_supported(self):
        """Test that paper reading returns appropriate message"""
        result = self.searcher.read_paper("some_id")
        assert "doesn't support direct paper reading" in result

    def test_parse_paper_missing_elements(self):
        """Test parsing paper with missing required elements"""
        # Mock item without required elements
        mock_item = Mock()
        mock_item.find.return_value = None

        result = self.searcher._parse_paper(mock_item)
        assert result is None

    def test_search_with_year_filters(self):
        """Test search with year range filters"""
        with patch.object(self.searcher.session, "get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "<html><div>No results</div></html>"
            mock_get.return_value = mock_response

            with patch("time.sleep"):
                self.searcher.search("test", year_low=2020, year_high=2023)

            # Verify that year parameters were passed
            call_args = mock_get.call_args
            params = call_args[1]["params"]
            assert params["as_ylo"] == 2020
            assert params["as_yhi"] == 2023
