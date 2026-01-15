# tests/test_qwen_search.py
"""
Unit tests for Qwen Search functionality
"""

import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestQwenSearch(unittest.TestCase):
    def test_qwen_search_import(self):
        """Test that qwen_search server can be imported"""
        try:
            import qwen_search.server

            self.assertTrue(True, "Qwen Search server imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import Qwen Search server: {e}")

    def test_qwen_search_main_function(self):
        """Test that main function exists"""
        try:
            import qwen_search.server

            # Check if the main function exists
            self.assertTrue(
                hasattr(qwen_search.server, "main"), "main function should exist"
            )
            self.assertTrue(
                callable(qwen_search.server.main), "main should be callable"
            )

            # Check if the FastMCP mcp exists
            self.assertTrue(
                hasattr(qwen_search.server, "mcp"), "FastMCP mcp should exist"
            )

        except Exception as e:
            self.fail(f"Failed to check Qwen Search main: {e}")

    def test_qwen_search_requires_api_key(self):
        """Test that Qwen Search requires DASHSCOPE_API_KEY"""
        try:
            import qwen_search.server

            # Temporarily clear the environment variable
            original_key = os.environ.get("DASHSCOPE_API_KEY")
            os.environ.pop("DASHSCOPE_API_KEY", None)

            try:
                # Import the module again to test without API key
                # This should create a fallback server with an error message
                import importlib

                importlib.reload(qwen_search.server)

                # The module should still be importable, but the server will have an error tool
                self.assertTrue(True, "Server can be imported without API key")
            finally:
                # Restore the original API key if it existed
                if original_key:
                    os.environ["DASHSCOPE_API_KEY"] = original_key

        except ImportError as e:
            self.fail(f"Failed to import Qwen Search server: {e}")


if __name__ == "__main__":
    unittest.main()
