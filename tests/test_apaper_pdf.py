# tests/test_apaper_pdf.py
"""
Unit tests for APaper PDF reading functionality
"""
import unittest
import sys
import os
from pathlib import Path
import tempfile

# Add the src directory to the path so we can import our modules  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from apaper.utils.pdf_reader import read_pdf, _normalize_page_range


class TestAPaperPDFReader(unittest.TestCase):
    
    def test_normalize_page_range(self):
        """Test page range normalization"""
        # Test default values
        start_idx, end_idx = _normalize_page_range(None, None, 10)
        self.assertEqual(start_idx, 0)  # 0-indexed
        self.assertEqual(end_idx, 9)   # 0-indexed
        
        # Test specific range
        start_idx, end_idx = _normalize_page_range(2, 5, 10)
        self.assertEqual(start_idx, 1)  # 2-1 = 1
        self.assertEqual(end_idx, 4)   # 5-1 = 4
        
        # Test clamp end page
        start_idx, end_idx = _normalize_page_range(5, 20, 10)
        self.assertEqual(start_idx, 4)  # 5-1 = 4
        self.assertEqual(end_idx, 9)   # clamped to 10-1 = 9
    
    def test_normalize_page_range_validation(self):
        """Test page range validation errors"""
        # Test invalid start page
        with self.assertRaises(ValueError):
            _normalize_page_range(0, 5, 10)
        
        # Test invalid end page  
        with self.assertRaises(ValueError):
            _normalize_page_range(1, 0, 10)
        
        # Test start > end
        with self.assertRaises(ValueError):
            _normalize_page_range(5, 3, 10)
        
        # Test start > total pages
        with self.assertRaises(ValueError):
            _normalize_page_range(15, 20, 10)
    
    def test_read_pdf_invalid_source(self):
        """Test reading PDF with invalid source"""
        with self.assertRaises(Exception):
            read_pdf("/nonexistent/file.pdf")
        
        with self.assertRaises(Exception):
            read_pdf("not_a_pdf.txt")
    
    def test_read_pdf_invalid_url(self):
        """Test reading PDF with invalid URL"""
        with self.assertRaises(Exception):
            read_pdf("https://invalid-url-that-does-not-exist.com/file.pdf")


if __name__ == "__main__":
    unittest.main()