"""Tests for Crossref searcher"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.all_in_mcp.academic_platforms.crossref import CrossrefSearcher


class TestCrossrefSearcher:
    """Test cases for CrossrefSearcher"""

    def setup_method(self):
        """Set up test fixtures"""
        self.searcher = CrossrefSearcher()

        # Mock response data
        self.mock_search_response = {
            "message": {
                "items": [
                    {
                        "DOI": "10.1000/test.doi.1",
                        "title": ["Test Quantum Computing Paper"],
                        "author": [
                            {"given": "John", "family": "Doe"},
                            {"given": "Jane", "family": "Smith"},
                        ],
                        "abstract": "This is a test abstract about quantum computing research.",
                        "published-print": {"date-parts": [[2022, 5, 15]]},
                        "URL": "https://example.com/paper1",
                        "container-title": ["Test Quantum Journal"],
                        "volume": "42",
                        "issue": "3",
                        "page": "123-145",
                        "subject": ["Physics", "Computer Science"],
                        "is-referenced-by-count": 25,
                        "type": "journal-article",
                        "publisher": "Test Publisher",
                        "ISSN": ["1234-5678"],
                        "link": [
                            {
                                "content-type": "application/pdf",
                                "URL": "https://example.com/paper1.pdf",
                            }
                        ],
                    },
                    {
                        "DOI": "10.1000/test.doi.2",
                        "title": ["Another Quantum Paper"],
                        "author": [{"given": "Alice", "family": "Wilson"}],
                        "abstract": "Another test abstract.",
                        "published-online": {"date-parts": [[2021, 8, 10]]},
                        "URL": "https://example.com/paper2",
                        "container-title": ["Second Test Journal"],
                        "is-referenced-by-count": 10,
                        "type": "journal-article",
                    },
                ]
            }
        }

        self.mock_single_work_response = {
            "message": {
                "DOI": "10.1000/test.doi.1",
                "title": ["Test Quantum Computing Paper"],
                "author": [
                    {"given": "John", "family": "Doe"},
                    {"given": "Jane", "family": "Smith"},
                ],
                "abstract": "This is a test abstract about quantum computing research.",
                "published-print": {"date-parts": [[2022, 5, 15]]},
                "URL": "https://example.com/paper1",
                "container-title": ["Test Quantum Journal"],
                "volume": "42",
                "issue": "3",
                "page": "123-145",
                "subject": ["Physics", "Computer Science"],
                "is-referenced-by-count": 25,
                "type": "journal-article",
                "publisher": "Test Publisher",
                "ISSN": ["1234-5678"],
                "link": [
                    {
                        "content-type": "application/pdf",
                        "URL": "https://example.com/paper1.pdf",
                    }
                ],
            }
        }

    @patch("httpx.Client.get")
    def test_search_basic(self, mock_get):
        """Test basic search functionality"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_search_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        papers = self.searcher.search("quantum computing", max_results=3)

        assert isinstance(papers, list)
        assert len(papers) == 2  # Our mock data has 2 papers

        paper = papers[0]
        assert paper.title == "Test Quantum Computing Paper"
        assert paper.authors == ["John Doe", "Jane Smith"]
        assert paper.doi == "10.1000/test.doi.1"
        assert paper.source == "crossref"
        assert paper.citations == 25
        assert paper.published_date == datetime(2022, 5, 15)

        # Verify the API call was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "query" in call_args[1]["params"]
        assert call_args[1]["params"]["query"] == "quantum computing"

    @patch("httpx.Client.get")
    def test_search_with_year_filter(self, mock_get):
        """Test search with year filtering"""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_search_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        papers = self.searcher.search(
            "machine learning", max_results=5, year_min=2020, year_max=2023
        )

        assert isinstance(papers, list)

        # Verify the API call included year filters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "filter" in call_args[1]["params"]
        filter_param = call_args[1]["params"]["filter"]
        assert "from-pub-date:2020" in filter_param
        assert "until-pub-date:2023" in filter_param

    def test_search_empty_query(self):
        """Test search with empty query"""
        papers = self.searcher.search("", max_results=5)
        assert papers == []

    @patch("httpx.Client.get")
    def test_search_by_doi(self, mock_get):
        """Test searching by DOI"""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_single_work_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        doi_paper = self.searcher.search_by_doi("10.1000/test.doi.1")

        assert doi_paper is not None
        assert doi_paper.doi == "10.1000/test.doi.1"
        assert doi_paper.title == "Test Quantum Computing Paper"

        # Verify the API call was made to the correct endpoint
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "works/10.1000%2Ftest.doi.1" in call_args[0][0]

    def test_download_pdf_missing_id(self):
        """Test PDF download with missing paper ID"""
        result = self.searcher.download_pdf("", "./downloads")
        assert result.startswith("Error:")

    def test_read_paper_missing_id(self):
        """Test paper reading with missing paper ID"""
        result = self.searcher.read_paper("", "./downloads")
        assert result.startswith("Error:")

    @patch("httpx.Client.get")
    def test_sort_options(self, mock_get):
        """Test different sort options"""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_search_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        for sort_by in ["relevance", "published", "indexed", "updated"]:
            papers = self.searcher.search(
                "artificial intelligence", max_results=2, sort_by=sort_by
            )
            assert isinstance(papers, list)

            # Verify the sort parameter was passed correctly
            call_args = mock_get.call_args
            assert call_args[1]["params"]["sort"] == sort_by

    @patch("httpx.Client.get")
    def test_search_api_error(self, mock_get):
        """Test handling of API errors"""
        mock_get.side_effect = Exception("Network error")

        papers = self.searcher.search("test query", max_results=5)
        assert papers == []

    @patch("httpx.Client.get")
    def test_download_pdf_with_doi(self, mock_get):
        """Test PDF download with DOI"""
        # Mock the work details response
        work_response = Mock()
        work_response.json.return_value = self.mock_single_work_response
        work_response.raise_for_status.return_value = None

        # Mock the PDF download response
        pdf_response = Mock()
        pdf_response.content = b"fake pdf content"
        pdf_response.raise_for_status.return_value = None

        mock_get.side_effect = [work_response, pdf_response]

        with patch("builtins.open", create=True) as mock_open:
            with patch("pathlib.Path.mkdir"):
                result = self.searcher.download_pdf("10.1000/test.doi.1", "./downloads")

                assert not result.startswith("Error:")
                assert "crossref_10_1000_test_doi_1.pdf" in result
                mock_open.assert_called_once()

    @patch("httpx.Client.get")
    def test_parse_work_with_minimal_data(self, mock_get):
        """Test parsing work with minimal required data"""
        minimal_work = {
            "message": {
                "items": [{"title": ["Minimal Paper"], "DOI": "10.1000/minimal"}]
            }
        }

        mock_response = Mock()
        mock_response.json.return_value = minimal_work
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        papers = self.searcher.search("test", max_results=1)

        assert len(papers) == 1
        assert papers[0].title == "Minimal Paper"
        assert papers[0].doi == "10.1000/minimal"
        assert papers[0].authors == []  # Should default to empty list
