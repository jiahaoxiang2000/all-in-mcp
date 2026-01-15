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

    def test_qwen_search_client_import(self):
        """Test that qwen_search client can be imported"""
        try:
            from qwen_search.client import QwenSearchClient, QwenSearchError

            # Test instantiation will fail without API key, but we can check the class exists
            self.assertIsNotNone(QwenSearchClient)
            self.assertIsNotNone(QwenSearchError)

        except ImportError as e:
            self.fail(f"Failed to import Qwen Search client: {e}")

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

            # Check if the FastMCP app exists
            self.assertTrue(
                hasattr(qwen_search.server, "mcp"), "FastMCP mcp should exist"
            )

        except Exception as e:
            self.fail(f"Failed to check Qwen Search main: {e}")

    def test_qwen_search_client_without_api_key(self):
        """Test that QwenSearchClient raises error without API key"""
        try:
            from qwen_search.client import QwenSearchClient, QwenSearchError

            # Temporarily clear the environment variable
            original_key = os.environ.get("DASHSCOPE_API_KEY")
            os.environ.pop("DASHSCOPE_API_KEY", None)

            try:
                # This should raise an error
                with self.assertRaises(QwenSearchError) as context:
                    client = QwenSearchClient()

                self.assertIn(
                    "DASHSCOPE_API_KEY not found",
                    str(context.exception),
                )
            finally:
                # Restore the original API key if it existed
                if original_key:
                    os.environ["DASHSCOPE_API_KEY"] = original_key

        except ImportError as e:
            self.fail(f"Failed to import Qwen Search client: {e}")


if __name__ == "__main__":
    unittest.main()
