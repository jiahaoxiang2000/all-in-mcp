# tests/test_mcp_server.py
"""
Unit tests for the MCP server functionality
"""
import unittest
import asyncio
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from all_in_mcp.server import handle_list_tools, handle_call_tool
import mcp.types as types


class TestMCPServer(unittest.TestCase):

    def test_list_tools(self):
        """Test that list_tools returns expected tools"""

        async def run_test():
            tools = await handle_list_tools()
            self.assertIsInstance(tools, list)
            self.assertGreater(len(tools), 0)

            # Check that all expected tools are present
            tool_names = [tool.name for tool in tools]
            expected_tools = [
                "encode-base64",
                "search-iacr-papers",
                "download-iacr-paper",
                "read-iacr-paper",
            ]

            for expected_tool in expected_tools:
                self.assertIn(expected_tool, tool_names)

        asyncio.run(run_test())

    def test_encode_base64_tool(self):
        """Test the base64 encoding tool"""

        async def run_test():
            result = await handle_call_tool("encode-base64", {"text": "Hello World"})
            result_list = list(result)

            self.assertEqual(len(result_list), 1)
            self.assertIsInstance(result_list[0], types.TextContent)
            if isinstance(result_list[0], types.TextContent):
                self.assertIn("SGVsbG8gV29ybGQ=", result_list[0].text)

        asyncio.run(run_test())

    def test_search_iacr_papers_tool(self):
        """Test the IACR search tool"""

        async def run_test():
            result = await handle_call_tool(
                "search-iacr-papers", {"query": "cryptography", "max_results": 2}
            )
            result_list = list(result)

            self.assertEqual(len(result_list), 1)
            self.assertIsInstance(result_list[0], types.TextContent)
            if isinstance(result_list[0], types.TextContent):
                # Should contain some search results
                self.assertGreater(len(result_list[0].text), 0)

        asyncio.run(run_test())

    def test_invalid_tool_name(self):
        """Test calling an invalid tool name"""

        async def run_test():
            result = await handle_call_tool("invalid-tool", {})
            result_list = list(result)

            self.assertEqual(len(result_list), 1)
            self.assertIsInstance(result_list[0], types.TextContent)
            if isinstance(result_list[0], types.TextContent):
                self.assertIn("Unknown tool", result_list[0].text)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
