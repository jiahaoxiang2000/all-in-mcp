"""
Qwen Search - Web Search Module

A specialized module for web search using the Qwen/Dashscope API.
Provides tools for searching the web with the Dashscope SSE-based search API.
"""

from .server import main

__version__ = "0.1.0"
__all__ = ["main"]
