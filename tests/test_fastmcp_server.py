# tests/test_fastmcp_server.py
"""
Unit tests for FastMCP server functionality
"""
import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestFastMCPServer(unittest.TestCase):
    
    def test_all_in_mcp_import(self):
        """Test that all-in-mcp server can be imported"""
        try:
            import all_in_mcp.server
            self.assertTrue(True, "all-in-mcp server imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import all-in-mcp server: {e}")
    
    def test_apaper_import(self):
        """Test that apaper server can be imported"""
        try:
            import apaper.server
            self.assertTrue(True, "APaper server imported successfully") 
        except ImportError as e:
            self.fail(f"Failed to import APaper server: {e}")
    
    def test_apaper_platforms_import(self):
        """Test that all APaper platforms can be imported"""
        try:
            from apaper.platforms import (
                IACRSearcher,
                CryptoBibSearcher,
                CrossrefSearcher,
                GoogleScholarSearcher
            )
            
            # Test instantiation
            iacr = IACRSearcher()
            cryptobib = CryptoBibSearcher()
            crossref = CrossrefSearcher()
            google = GoogleScholarSearcher()
            
            self.assertIsNotNone(iacr)
            self.assertIsNotNone(cryptobib) 
            self.assertIsNotNone(crossref)
            self.assertIsNotNone(google)
            
        except ImportError as e:
            self.fail(f"Failed to import APaper platforms: {e}")
    
    def test_apaper_models_import(self):
        """Test that APaper models can be imported"""
        try:
            from apaper.models import Paper
            from apaper.utils import read_pdf
            
            self.assertIsNotNone(Paper)
            self.assertIsNotNone(read_pdf)
            
        except ImportError as e:
            self.fail(f"Failed to import APaper models: {e}")
    
    def test_fastmcp_tools_defined(self):
        """Test that FastMCP tools are properly defined"""
        try:
            import all_in_mcp.server as server
            
            # Check if the main function exists
            self.assertTrue(hasattr(server, 'main'), "main function should exist")
            self.assertTrue(callable(server.main), "main should be callable")
            
            # Check if the FastMCP app exists
            self.assertTrue(hasattr(server, 'app'), "FastMCP app should exist")
            
        except Exception as e:
            self.fail(f"Failed to check FastMCP tools: {e}")


if __name__ == "__main__":
    unittest.main()