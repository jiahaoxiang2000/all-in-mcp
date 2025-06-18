# IACR ePrint Archive Integration

This document describes the integration with the IACR ePrint Archive for academic paper search, download, and reading functionality.

## Overview

The IACR (International Association for Cryptologic Research) ePrint Archive is a repository for cryptography and information security research papers. Our integration provides:

- Search functionality across all papers
- PDF download capabilities
- Text extraction from papers
- Metadata parsing

## Features

### Search Capabilities

The search function queries the IACR archive and returns:

- Paper titles
- Author information
- Publication dates
- Abstracts
- Direct URLs to papers
- PDF download links
- Keywords and categories

### Download Functionality

- Direct PDF downloads from IACR servers
- Automatic file naming based on paper ID
- Configurable save directories
- Error handling for unavailable papers

### Text Extraction

- Full text extraction from downloaded PDFs
- Formatted output with metadata
- Handling of various PDF formats
- Error recovery for corrupted files

## Technical Implementation

### API Endpoints

The IACR integration uses:

- **Search API**: `https://eprint.iacr.org/search`
- **Paper URLs**: `https://eprint.iacr.org/YYYY/NNNN`
- **PDF URLs**: `https://eprint.iacr.org/YYYY/NNNN.pdf`

### Data Structure

Papers are represented using the standardized `Paper` class:

```python
@dataclass
class Paper:
    paper_id: str              # Format: "YYYY/NNNN"
    title: str                 # Full paper title
    authors: List[str]         # List of author names
    abstract: str              # Paper abstract
    url: str                   # Paper page URL
    pdf_url: str               # Direct PDF URL
    published_date: datetime   # Publication date
    source: str                # Always "iacr"
    categories: List[str]      # Subject categories
    keywords: List[str]        # Extracted keywords
    doi: str                   # DOI if available
```

### Error Handling

The implementation handles:

- Network connectivity issues
- Invalid paper IDs
- PDF download failures
- Text extraction errors
- Rate limiting

### Rate Limiting

To be respectful to IACR servers:

- Search requests are throttled
- PDF downloads include delays
- Maximum concurrent requests limited
- Retry logic with exponential backoff

## Usage Examples

### Basic Search

```python
from all_in_mcp.academic_platforms.iacr import IACRSearcher

searcher = IACRSearcher()
papers = searcher.search("zero knowledge", max_results=10)

for paper in papers:
    print(f"{paper.title} ({paper.paper_id})")
```

### Download and Read

```python
# Download a specific paper
pdf_path = searcher.download_pdf("2023/1234", "./downloads")

# Extract text content
text_content = searcher.read_paper("2023/1234", "./downloads")
print(text_content[:500])  # First 500 characters
```

## Configuration

### Environment Variables

- `IACR_DOWNLOAD_DIR`: Default download directory
- `IACR_MAX_RETRIES`: Maximum retry attempts
- `IACR_TIMEOUT`: Request timeout in seconds

### Default Settings

```python
DEFAULT_CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "download_dir": "./downloads",
    "user_agent": "All-in-MCP Academic Search"
}
```

## Limitations

### Current Limitations

- Search is limited to title and abstract matching
- No advanced search operators
- PDF extraction may fail for scanned documents
- Large papers may take time to process

### Future Enhancements

- Advanced search with filters
- Author-based search
- Citation network analysis
- Full-text search capabilities
- Batch download operations

## Troubleshooting

### Common Issues

**Search returns no results**:

- Check query spelling
- Try broader search terms
- Verify network connectivity

**PDF download fails**:

- Check paper ID format (YYYY/NNNN)
- Verify paper exists on IACR
- Check file system permissions

**Text extraction incomplete**:

- PDF may be image-based
- Try re-downloading the PDF
- Check for PDF corruption

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show detailed information about:

- HTTP requests and responses
- PDF processing steps
- Error details and stack traces
