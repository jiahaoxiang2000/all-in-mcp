"""
Tests for PDF reading functionality
"""

import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.all_in_mcp.paper import (
    Paper,
    read_pdf,
    _read_pdf_from_file,
    _read_pdf_from_url,
)


class TestReadPdfFunctionality:
    """Test cases for PDF reading functionality"""

    def test_paper_read_content_no_pdf_url(self):
        """Test that Paper.read_content() raises error when no PDF URL is available"""
        paper = Paper(
            paper_id="test-001",
            title="Test Paper",
            authors=["Test Author"],
            abstract="Test abstract",
            doi="10.1000/test",
            published_date=datetime.now(),
            pdf_url="",  # Empty PDF URL
            url="https://example.com",
            source="test",
        )

        with pytest.raises(ValueError, match="No PDF URL available for this paper"):
            paper.read_content()

    def test_read_pdf_invalid_source_type(self):
        """Test that read_pdf raises error for invalid source type"""
        with pytest.raises(
            Exception,
            match="Failed to read PDF from 123: pdf_source must be a string or Path object",
        ):
            read_pdf(123)  # type: ignore  # Invalid type for testing

    def test_read_pdf_from_file_not_exists(self):
        """Test that _read_pdf_from_file raises error for non-existent file"""
        non_existent_file = Path("/tmp/does_not_exist.pdf")

        with pytest.raises(FileNotFoundError, match="PDF file not found"):
            _read_pdf_from_file(non_existent_file)

    def test_read_pdf_from_file_wrong_extension(self):
        """Test that _read_pdf_from_file raises error for non-PDF files"""
        # Create a temporary non-PDF file
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            with pytest.raises(ValueError, match="File must have .pdf extension"):
                _read_pdf_from_file(tmp_path)
        finally:
            tmp_path.unlink()  # Clean up

    @patch("src.all_in_mcp.paper.httpx.Client")
    def test_read_pdf_from_url_success(self, mock_client):
        """Test successful PDF reading from URL"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \n0000000179 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n235\n%%EOF"
        mock_response.headers = {"content-type": "application/pdf"}
        mock_response.raise_for_status.return_value = None

        mock_client_instance = mock_client.return_value.__enter__.return_value
        mock_client_instance.get.return_value = mock_response

        # This should not raise an exception, though the content might be empty
        # since the mock PDF doesn't have extractable text
        result = _read_pdf_from_url("https://example.com/test.pdf")
        assert isinstance(result, str)

    @patch("src.all_in_mcp.paper.httpx.Client")
    def test_read_pdf_from_url_invalid_pdf(self, mock_client):
        """Test error handling for invalid PDF from URL"""
        # Mock the response with non-PDF content
        mock_response = MagicMock()
        mock_response.content = b"This is not a PDF file"
        mock_response.headers = {"content-type": "text/plain"}
        mock_response.raise_for_status.return_value = None

        mock_client_instance = mock_client.return_value.__enter__.return_value
        mock_client_instance.get.return_value = mock_response

        with pytest.raises(Exception, match="URL does not point to a valid PDF file"):
            _read_pdf_from_url("https://example.com/not-a-pdf.txt")

    @patch("src.all_in_mcp.paper.httpx.Client")
    def test_read_pdf_from_url_network_error(self, mock_client):
        """Test network error handling"""
        import httpx

        mock_client_instance = mock_client.return_value.__enter__.return_value
        mock_client_instance.get.side_effect = httpx.RequestError("Network error")

        with pytest.raises(Exception, match="Network error downloading PDF"):
            _read_pdf_from_url("https://example.com/test.pdf")

    def test_read_pdf_url_detection(self):
        """Test URL detection in read_pdf function"""
        # Test HTTP URL
        with patch("src.all_in_mcp.paper._read_pdf_from_url") as mock_url_reader:
            mock_url_reader.return_value = "Mock PDF content"
            result = read_pdf("http://example.com/test.pdf")
            assert result == "Mock PDF content"
            mock_url_reader.assert_called_once_with("http://example.com/test.pdf")

        # Test HTTPS URL
        with patch("src.all_in_mcp.paper._read_pdf_from_url") as mock_url_reader:
            mock_url_reader.return_value = "Mock PDF content"
            result = read_pdf("https://example.com/test.pdf")
            assert result == "Mock PDF content"
            mock_url_reader.assert_called_once_with("https://example.com/test.pdf")

    def test_read_pdf_local_file_detection(self):
        """Test local file detection in read_pdf function"""
        with patch("src.all_in_mcp.paper._read_pdf_from_file") as mock_file_reader:
            mock_file_reader.return_value = "Mock PDF content"
            result = read_pdf("/path/to/local/file.pdf")
            assert result == "Mock PDF content"
            mock_file_reader.assert_called_once()

    def test_paper_with_pdf_url_success(self):
        """Test Paper.read_content() with valid PDF URL"""
        paper = Paper(
            paper_id="test-001",
            title="Test Paper",
            authors=["Test Author"],
            abstract="Test abstract",
            doi="10.1000/test",
            published_date=datetime.now(),
            pdf_url="https://example.com/test.pdf",
            url="https://example.com",
            source="test",
        )

        with patch("src.all_in_mcp.paper.read_pdf") as mock_read_pdf:
            mock_read_pdf.return_value = "Mock PDF content"
            result = paper.read_content()
            assert result == "Mock PDF content"
            mock_read_pdf.assert_called_once_with("https://example.com/test.pdf")
