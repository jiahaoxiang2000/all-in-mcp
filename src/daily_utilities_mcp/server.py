import asyncio
import base64
import hashlib
import json
import os
import platform
import re
import subprocess
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
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
        types.Tool(
            name="decode-base64",
            description="Decode Base64 text",
            inputSchema={
                "type": "object",
                "properties": {
                    "encoded": {
                        "type": "string",
                        "description": "Base64 text to decode",
                    },
                },
                "required": ["encoded"],
            },
        ),
        types.Tool(
            name="hash-text",
            description="Generate hash (MD5, SHA1, SHA256) of text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to hash"},
                    "algorithm": {
                        "type": "string",
                        "enum": ["md5", "sha1", "sha256"],
                        "description": "Hash algorithm to use",
                        "default": "sha256",
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="url-encode",
            description="URL encode text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to URL encode"},
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="url-decode",
            description="URL decode text",
            inputSchema={
                "type": "object",
                "properties": {
                    "encoded": {
                        "type": "string",
                        "description": "URL encoded text to decode",
                    },
                },
                "required": ["encoded"],
            },
        ),
        types.Tool(
            name="format-json",
            description="Format and validate JSON text",
            inputSchema={
                "type": "object",
                "properties": {
                    "json_text": {
                        "type": "string",
                        "description": "JSON text to format",
                    },
                    "indent": {
                        "type": "integer",
                        "description": "Indentation spaces",
                        "default": 2,
                    },
                },
                "required": ["json_text"],
            },
        ),
        types.Tool(
            name="timestamp-now",
            description="Get current timestamp in various formats",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["unix", "iso", "human"],
                        "description": "Timestamp format",
                        "default": "iso",
                    },
                    "timezone": {
                        "type": "string",
                        "description": "Timezone (e.g., UTC, local)",
                        "default": "UTC",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="system-info",
            description="Get system information",
            inputSchema={
                "type": "object",
                "properties": {
                    "details": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["platform", "python", "cpu", "memory", "disk"],
                        },
                        "description": "System details to retrieve",
                        "default": ["platform", "python"],
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="regex-match",
            description="Test regex patterns against text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to test"},
                    "pattern": {"type": "string", "description": "Regex pattern"},
                    "flags": {
                        "type": "string",
                        "description": "Regex flags (i, m, s, x)",
                        "default": "",
                    },
                },
                "required": ["text", "pattern"],
            },
        ),
        types.Tool(
            name="count-words",
            description="Count words, characters, and lines in text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to analyze"},
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
    Handle tool execution requests for daily utilities.
    """
    if not arguments:
        arguments = {}

    try:
        if name == "encode-base64":
            text = arguments.get("text", "")
            encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            return [types.TextContent(type="text", text=f"Base64 encoded: {encoded}")]

        elif name == "decode-base64":
            encoded = arguments.get("encoded", "")
            try:
                decoded = base64.b64decode(encoded).decode("utf-8")
                return [
                    types.TextContent(type="text", text=f"Base64 decoded: {decoded}")
                ]
            except Exception as e:
                return [
                    types.TextContent(
                        type="text", text=f"Error decoding Base64: {str(e)}"
                    )
                ]

        elif name == "hash-text":
            text = arguments.get("text", "")
            algorithm = arguments.get("algorithm", "sha256").lower()

            if algorithm == "md5":
                hash_obj = hashlib.md5(text.encode("utf-8"))
            elif algorithm == "sha1":
                hash_obj = hashlib.sha1(text.encode("utf-8"))
            elif algorithm == "sha256":
                hash_obj = hashlib.sha256(text.encode("utf-8"))
            else:
                return [
                    types.TextContent(
                        type="text", text="Error: Unsupported hash algorithm"
                    )
                ]

            hash_value = hash_obj.hexdigest()
            return [
                types.TextContent(
                    type="text", text=f"{algorithm.upper()} hash: {hash_value}"
                )
            ]

        elif name == "url-encode":
            text = arguments.get("text", "")
            encoded = urllib.parse.quote(text)
            return [types.TextContent(type="text", text=f"URL encoded: {encoded}")]

        elif name == "url-decode":
            encoded = arguments.get("encoded", "")
            try:
                decoded = urllib.parse.unquote(encoded)
                return [types.TextContent(type="text", text=f"URL decoded: {decoded}")]
            except Exception as e:
                return [
                    types.TextContent(type="text", text=f"Error decoding URL: {str(e)}")
                ]

        elif name == "format-json":
            json_text = arguments.get("json_text", "")
            indent = arguments.get("indent", 2)
            try:
                parsed = json.loads(json_text)
                formatted = json.dumps(parsed, indent=indent, ensure_ascii=False)
                return [
                    types.TextContent(type="text", text=f"Formatted JSON:\n{formatted}")
                ]
            except json.JSONDecodeError as e:
                return [types.TextContent(type="text", text=f"Invalid JSON: {str(e)}")]

        elif name == "timestamp-now":
            format_type = arguments.get("format", "iso")
            timezone_str = arguments.get("timezone", "UTC")

            now = datetime.now(timezone.utc)

            if format_type == "unix":
                result = str(int(now.timestamp()))
            elif format_type == "iso":
                result = now.isoformat()
            elif format_type == "human":
                result = now.strftime("%Y-%m-%d %H:%M:%S UTC")
            else:
                result = now.isoformat()

            return [
                types.TextContent(
                    type="text", text=f"Current timestamp ({format_type}): {result}"
                )
            ]

        elif name == "system-info":
            details = arguments.get("details", ["platform", "python"])
            info_parts = []

            if "platform" in details:
                info_parts.append(f"Platform: {platform.platform()}")
                info_parts.append(f"System: {platform.system()}")
                info_parts.append(f"Architecture: {platform.architecture()[0]}")

            if "python" in details:
                info_parts.append(f"Python version: {platform.python_version()}")

            if "cpu" in details:
                info_parts.append(f"Processor: {platform.processor()}")

            if "memory" in details or "disk" in details:
                try:
                    import psutil

                    if "memory" in details:
                        memory = psutil.virtual_memory()
                        info_parts.append(
                            f"Memory: {memory.total // (1024**3)} GB total"
                        )
                    if "disk" in details:
                        disk = psutil.disk_usage("/")
                        info_parts.append(f"Disk: {disk.total // (1024**3)} GB total")
                except ImportError:
                    info_parts.append("Note: Install psutil for memory/disk info")

            result = "\n".join(info_parts)
            return [
                types.TextContent(type="text", text=f"System Information:\n{result}")
            ]

        elif name == "regex-match":
            text = arguments.get("text", "")
            pattern = arguments.get("pattern", "")
            flags_str = arguments.get("flags", "")

            # Convert flag string to regex flags
            flags = 0
            if "i" in flags_str.lower():
                flags |= re.IGNORECASE
            if "m" in flags_str.lower():
                flags |= re.MULTILINE
            if "s" in flags_str.lower():
                flags |= re.DOTALL
            if "x" in flags_str.lower():
                flags |= re.VERBOSE

            try:
                matches = re.findall(pattern, text, flags)
                if matches:
                    result = f"Found {len(matches)} match(es):\n" + "\n".join(
                        f"- {match}" for match in matches
                    )
                else:
                    result = "No matches found"
                return [types.TextContent(type="text", text=result)]
            except re.error as e:
                return [types.TextContent(type="text", text=f"Regex error: {str(e)}")]

        elif name == "count-words":
            text = arguments.get("text", "")

            # Count different metrics
            char_count = len(text)
            char_count_no_spaces = len(text.replace(" ", ""))
            word_count = len(text.split())
            line_count = len(text.splitlines())

            result = f"""Text Analysis:
- Characters (with spaces): {char_count}
- Characters (without spaces): {char_count_no_spaces}
- Words: {word_count}
- Lines: {line_count}"""

            return [types.TextContent(type="text", text=result)]

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
