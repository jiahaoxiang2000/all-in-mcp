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

## Google Scholar Search

### search-google-scholar-papers

Search academic papers from Google Scholar. This provides broad coverage across multiple academic disciplines and includes citation information.

**Parameters:**

- `query` (string, required): Search query string (e.g., 'machine learning', 'neural networks')
- `max_results` (integer, optional): Maximum number of results to return (default: 10)
- `year_low` (integer, optional): Minimum publication year for filtering
- `year_high` (integer, optional): Maximum publication year for filtering

**Returns:**

- List of papers with metadata (title, authors, citations, year, URL, abstract)

**Example:**

```json
{
  "name": "search-google-scholar-papers",
  "arguments": {
    "query": "deep learning transformers",
    "max_results": 5,
    "year_low": 2020,
    "year_high": 2024
  }
}
```

**Response:**

```
Found 3 Google Scholar papers for query 'deep learning transformers' in year range (2020-2024):

1. **Attention Is All You Need**
   - Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar
   - Citations: 85234
   - Year: 2017
   - URL: https://papers.nips.cc/paper/7181-attention-is-all-you-need
   - Abstract: The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...
```

**Limitations:**

- No direct PDF downloads (redirects to publisher websites)
- Rate limiting may apply for frequent requests
- Results may vary based on geographic location

## DBLP Bibliography Search

### search-dblp-papers

Search DBLP computer science bibliography database for papers. DBLP is a comprehensive bibliography database for computer science publications.

**Parameters:**

- `query` (string, required): Search query string (supports boolean 'and'/'or' operators)
- `max_results` (integer, optional): Maximum number of results to return (default: 10)
- `year_from` (integer, optional): Lower bound for publication year
- `year_to` (integer, optional): Upper bound for publication year
- `venue_filter` (string, optional): Case-insensitive substring filter for venues (e.g., 'ICLR', 'NeurIPS')
- `include_bibtex` (boolean, optional): Whether to include BibTeX entries in results (default: false)

**Returns:**

- List of papers with metadata (title, authors, venue, year, DOI, URL, and optionally BibTeX)

**Example:**

```json
{
  "name": "search-dblp-papers",
  "arguments": {
    "query": "attention transformer",
    "max_results": 5,
    "year_from": 2017,
    "include_bibtex": true
  }
}
```

**Response:**

```text
Found 5 DBLP papers for query 'attention transformer' with filters: year range (2017-latest):

1. **Attention Is All You Need**
   - DBLP Key: conf/nips/VaswaniSPUJGKP17
   - Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, ...
   - Venue: NeurIPS
   - Year: 2017
   - DOI: 10.5555/3295222.3295349
   - BibTeX:
   @inproceedings{VaswaniSPUJGKP17,
     author = {Ashish Vaswani and ...},
     title = {Attention Is All You Need},
      ...
    }
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
