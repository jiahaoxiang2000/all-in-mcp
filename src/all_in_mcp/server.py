import base64
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

server = Server("all-in-mcp")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available daily utility tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="encode-base64",
            description="Encode text to Base64",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to encode"},
                },
                "required": ["text"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests for the Base64 encoding utility.
    """
    if not arguments:
        arguments = {}

    try:
        if name == "encode-base64":
            text = arguments.get("text", "")
            encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            return [types.TextContent(type="text", text=f"Base64 encoded: {encoded}")]
        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [
            types.TextContent(type="text", text=f"Error executing {name}: {str(e)}")
        ]


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="all-in-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
