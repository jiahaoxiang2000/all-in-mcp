"""
Qwen Search - Web Search Module

A specialized module for web search using the Qwen/Dashscope API.
Provides tools for searching the web with the Dashscope SSE-based search API.

This module can be used in two ways:
1. As a standalone proxy server (run: qwen-search)
2. As part of the all-in-mcp proxy server (set QWEN_SEARCH=true)
"""

from .server import main

__version__ = "0.1.0"
__all__ = ["main"]
