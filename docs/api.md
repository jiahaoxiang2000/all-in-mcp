# API Reference

Complete API documentation for all tools available in the All-in-MCP server.

## Academic Paper Search

### search-iacr-papers

Search academic papers from IACR ePrint Archive.

**Parameters:**

- `query` (string, required): Search query
- `max_results` (integer, optional): Maximum number of results (default: 10)

**Returns:**

- List of papers with metadata (title, authors, abstract, URLs)

**Example:**

```json
{
  "name": "search-iacr-papers",
  "arguments": {
    "query": "zero knowledge",
    "max_results": 5
  }
}
```

**Response:**

```
Found 5 IACR papers for query 'zero knowledge':

1. **Paper Title**
   - Paper ID: 2025/1234
   - Authors: Author Names
   - URL: https://eprint.iacr.org/2025/1234
   - Abstract: Paper abstract...
```

### download-iacr-paper

Download PDF of an IACR ePrint paper.

**Parameters:**

- `paper_id` (string, required): IACR paper ID (e.g., "2023/1234")
- `save_path` (string, optional): Directory to save PDF (default: "./downloads")

**Returns:**

- Path to downloaded PDF file

**Example:**

```json
{
  "name": "download-iacr-paper",
  "arguments": {
    "paper_id": "2023/1234",
    "save_path": "./downloads"
  }
}
```

**Response:**

```
PDF downloaded successfully to: ./downloads/iacr_2023_1234.pdf
```

### read-iacr-paper

Read and extract text content from an IACR ePrint paper PDF.

**Parameters:**

- `paper_id` (string, required): IACR paper ID (e.g., "2023/1234")
- `save_path` (string, optional): Directory where PDF is saved (default: "./downloads")

**Returns:**

- Extracted text content from the PDF

**Example:**

```json
{
  "name": "read-iacr-paper",
  "arguments": {
    "paper_id": "2023/1234",
    "save_path": "./downloads"
  }
}
```

**Response:**

```
Title: Paper Title
Authors: Author Names
Published Date: 2023-XX-XX
URL: https://eprint.iacr.org/2023/1234
...
[Full extracted text content]
```

## Error Handling

All tools return error messages in case of failures:

**Common Error Types:**

- Invalid parameters
- Network connectivity issues
- File system errors
- API rate limiting
- Paper not found

**Error Response Format:**

```
Error executing [tool-name]: [error description]
```

## Rate Limiting

The server implements reasonable rate limiting to avoid overwhelming academic paper sources:

- IACR ePrint Archive: Respectful crawling with delays
- PDF downloads: Sequential processing to avoid server overload

## Data Formats

### Paper Object

Papers are returned with the following structure:

```json
{
  "paper_id": "2023/1234",
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "abstract": "Paper abstract text...",
  "url": "https://eprint.iacr.org/2023/1234",
  "pdf_url": "https://eprint.iacr.org/2023/1234.pdf",
  "published_date": "2023-XX-XX",
  "source": "iacr",
  "categories": ["cryptography"],
  "keywords": ["keyword1", "keyword2"]
}
```
