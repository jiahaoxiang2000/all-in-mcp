import pytest
import asyncio
import base64
from all_in_mcp.server import handle_call_tool
import mcp.types as types
from typing import List


class TestBase64Encoding:
    """Test cases for the Base64 encoding functionality."""

    @pytest.mark.asyncio
    async def test_encode_base64_simple_text(self):
        """Test encoding simple text to Base64."""
        # Test data
        text = "Hello, World!"
        expected_encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")

        # Call the function
        result = await handle_call_tool("encode-base64", {"text": text})
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        assert result_list[0].text == f"Base64 encoded: {expected_encoded}"

    @pytest.mark.asyncio
    async def test_encode_base64_empty_string(self):
        """Test encoding empty string to Base64."""
        # Test data
        text = ""
        expected_encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")

        # Call the function
        result = await handle_call_tool("encode-base64", {"text": text})
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        assert result_list[0].text == f"Base64 encoded: {expected_encoded}"

    @pytest.mark.asyncio
    async def test_encode_base64_special_characters(self):
        """Test encoding text with special characters to Base64."""
        # Test data
        text = "Hello! @#$%^&*()_+ 🌟"
        expected_encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")

        # Call the function
        result = await handle_call_tool("encode-base64", {"text": text})
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        assert result_list[0].text == f"Base64 encoded: {expected_encoded}"

    @pytest.mark.asyncio
    async def test_encode_base64_multiline_text(self):
        """Test encoding multiline text to Base64."""
        # Test data
        text = "Line 1\nLine 2\nLine 3"
        expected_encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")

        # Call the function
        result = await handle_call_tool("encode-base64", {"text": text})
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        assert result_list[0].text == f"Base64 encoded: {expected_encoded}"

    @pytest.mark.asyncio
    async def test_encode_base64_no_arguments(self):
        """Test encoding with no arguments (should use empty string)."""
        # Call the function with no arguments
        result = await handle_call_tool("encode-base64", {})
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        # Empty string encoded should be empty Base64
        expected_encoded = base64.b64encode("".encode("utf-8")).decode("utf-8")
        assert result_list[0].text == f"Base64 encoded: {expected_encoded}"

    @pytest.mark.asyncio
    async def test_encode_base64_none_arguments(self):
        """Test encoding with None arguments."""
        # Call the function with None arguments
        result = await handle_call_tool("encode-base64", None)
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        # Should use empty string as default
        expected_encoded = base64.b64encode("".encode("utf-8")).decode("utf-8")
        assert result_list[0].text == f"Base64 encoded: {expected_encoded}"

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        """Test calling an unknown tool."""
        # Call with unknown tool name
        result = await handle_call_tool("unknown-tool", {"text": "test"})
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        assert "Error executing unknown-tool" in result_list[0].text
        assert "Unknown tool: unknown-tool" in result_list[0].text

    @pytest.mark.asyncio
    async def test_encode_base64_large_text(self):
        """Test encoding large text to Base64."""
        # Test data - large text
        text = "A" * 1000  # 1000 character string
        expected_encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")

        # Call the function
        result = await handle_call_tool("encode-base64", {"text": text})
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        assert result_list[0].text == f"Base64 encoded: {expected_encoded}"

    @pytest.mark.asyncio
    async def test_encode_base64_unicode_text(self):
        """Test encoding Unicode text to Base64."""
        # Test data with various Unicode characters
        text = "Hello 世界 🌍 Ñiño café"
        expected_encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")

        # Call the function
        result = await handle_call_tool("encode-base64", {"text": text})
        result_list = list(result)  # Convert to list to enable indexing

        # Assertions
        assert len(result_list) == 1
        assert isinstance(result_list[0], types.TextContent)
        assert result_list[0].text == f"Base64 encoded: {expected_encoded}"
