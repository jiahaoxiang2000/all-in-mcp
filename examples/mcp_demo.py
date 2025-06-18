# examples/mcp_demo.py
"""
Demo of the MCP server with IACR paper search functionality
"""
import asyncio
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from all_in_mcp.server import handle_list_tools, handle_call_tool
import mcp.types as types


async def demo_mcp_server():
    """Demonstrate the MCP server functionality"""
    print("=== All-in-MCP Server Demo ===\n")

    # 1. List available tools
    print("1. Available tools:")
    tools = await handle_list_tools()
    for tool in tools:
        print(f"   - {tool.name}: {tool.description}")

    print(f"\nTotal tools available: {len(tools)}")

    # 2. Demo Base64 encoding
    print(f"\n2. Testing Base64 encoding:")
    result = await handle_call_tool("encode-base64", {"text": "Hello, MCP World!"})
    result_list = list(result)
    if result_list and isinstance(result_list[0], types.TextContent):
        print(f"   Result: {result_list[0].text}")

    # 3. Demo IACR search
    print(f"\n3. Testing IACR paper search:")
    result = await handle_call_tool(
        "search-iacr-papers", {"query": "zero knowledge", "max_results": 3}
    )
    result_list = list(result)
    if result_list and isinstance(result_list[0], types.TextContent):
        print(f"   Found papers: {result_list[0].text[:500]}...")

    # 4. Demo IACR download (using a known paper ID)
    print(f"\n4. Testing IACR paper download:")
    # Use a typical IACR paper ID format for demo
    demo_paper_id = "2023/1234"  # This might not exist, but shows the format
    result = await handle_call_tool(
        "download-iacr-paper", {"paper_id": demo_paper_id, "save_path": "./downloads"}
    )
    result_list = list(result)
    if result_list and isinstance(result_list[0], types.TextContent):
        print(f"   Download result: {result_list[0].text}")

    # 5. Demo IACR read
    print(f"\n5. Testing IACR paper reading:")
    result = await handle_call_tool(
        "read-iacr-paper", {"paper_id": demo_paper_id, "save_path": "./downloads"}
    )
    result_list = list(result)
    if result_list and isinstance(result_list[0], types.TextContent):
        content = result_list[0].text
        if len(content) > 200:
            print(f"   Read result: {content[:200]}...")
        else:
            print(f"   Read result: {content}")


if __name__ == "__main__":
    asyncio.run(demo_mcp_server())
