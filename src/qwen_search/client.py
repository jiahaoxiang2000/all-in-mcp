"""Qwen Search client for Dashscope API."""

import json
import os
from typing import Any
import httpx


class QwenSearchError(Exception):
    """Exception raised for Qwen Search API errors."""

    pass


class QwenSearchClient:
    """Client for Qwen/Dashscope Web Search API using SSE."""

    def __init__(self, api_key: str | None = None):
        """
        Initialize the Qwen Search client.

        Args:
            api_key: Dashscope API key. If None, reads from DASHSCOPE_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise QwenSearchError(
                "DASHSCOPE_API_KEY not found. Please set the DASHSCOPE_API_KEY "
                "environment variable or pass it to the constructor."
            )

        self.base_url = "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse"

    async def search(self, query: str, max_results: int = 10) -> str:
        """
        Search the web using Qwen/Dashscope API.

        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 10)

        Returns:
            Formatted search results as a string

        Raises:
            QwenSearchError: If the API request fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        payload = {
            "query": query,
            "max_results": max_results,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                )

                if response.status_code != 200:
                    error_msg = f"API request failed with status {response.status_code}"
                    try:
                        error_detail = response.json()
                        error_msg += f": {error_detail}"
                    except Exception:
                        error_msg += f": {response.text}"
                    raise QwenSearchError(error_msg)

                # Parse SSE response
                results = self._parse_sse_response(response.text)
                return self._format_results(query, results)

        except httpx.TimeoutException:
            raise QwenSearchError("Request timed out. Please try again.")
        except httpx.RequestError as e:
            raise QwenSearchError(f"Request failed: {str(e)}")

    def _parse_sse_response(self, sse_text: str) -> list[dict[str, Any]]:
        """
        Parse SSE (Server-Sent Events) response.

        Args:
            sse_text: Raw SSE response text

        Returns:
            List of parsed events as dictionaries
        """
        events = []
        current_event = {}

        for line in sse_text.split("\n"):
            line = line.strip()
            if not line:
                if current_event:
                    events.append(current_event)
                    current_event = {}
                continue

            if line.startswith("data: "):
                data_str = line[6:]
                try:
                    current_event["data"] = json.loads(data_str)
                except json.JSONDecodeError:
                    current_event["data"] = data_str
            elif line.startswith("event: "):
                current_event["event"] = line[7:]
            elif line.startswith("id: "):
                current_event["id"] = line[4:]

        if current_event:
            events.append(current_event)

        return events

    def _format_results(self, query: str, events: list[dict[str, Any]]) -> str:
        """
        Format search results into a readable string.

        Args:
            query: Original search query
            events: List of SSE events

        Returns:
            Formatted results string
        """
        if not events:
            return f"No results found for query: {query}"

        result_text = f"Search results for '{query}':\n\n"

        for i, event in enumerate(events, 1):
            data = event.get("data", {})

            if isinstance(data, dict):
                title = data.get("title", "Untitled")
                url = data.get("url", "")
                snippet = data.get("snippet", "")
                source = data.get("source", "")

                result_text += f"{i}. **{title}**\n"
                if url:
                    result_text += f"   - URL: {url}\n"
                if snippet:
                    result_text += f"   - Snippet: {snippet}\n"
                if source:
                    result_text += f"   - Source: {source}\n"
                result_text += "\n"
            elif isinstance(data, str):
                result_text += f"{i}. {data}\n\n"

        return result_text
