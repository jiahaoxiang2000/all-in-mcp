# CryptoBib Integration

This document describes the CryptoBib integration in the all-in-mcp server.

## Overview

CryptoBib (https://cryptobib.di.ens.fr/) is a comprehensive bibliography database for cryptography research papers. This integration allows searching through the CryptoBib database and retrieving BibTeX entries.

## Features

### Search Functionality

- Search through the entire CryptoBib database
- Case-insensitive search across all BibTeX fields
- Returns both parsed Paper objects and raw BibTeX entries
- Configurable result limits

### BibTeX Support

- Parse BibTeX entries into structured Paper objects
- Retrieve raw BibTeX entries for direct use
- Support for all standard BibTeX fields (author, title, booktitle, journal, year, etc.)
- Clean LaTeX formatting from titles and authors

## Available Tools

### search-cryptobib-papers

Search CryptoBib bibliography database for cryptography papers.

**Parameters:**

- `query` (required): Search query string (e.g., 'lattice', 'homomorphic encryption')
- `max_results` (optional, default: 10): Maximum number of results to return
- `return_bibtex` (optional, default: false): Whether to return raw BibTeX entries
- `force_download` (optional, default: false): Force download the newest crypto.bib file

**Examples:**

```json
{
  "query": "lattice cryptography",
  "max_results": 5,
  "return_bibtex": false
}
```

To get specific BibTeX entries, you can use targeted search queries with `return_bibtex=true`.

## Usage Examples

### Basic Search

```python
from all_in_mcp.academic_platforms.cryptobib import CryptoBibSearcher

searcher = CryptoBibSearcher()

# Search for papers
papers = searcher.search("homomorphic encryption", max_results=5)
for paper in papers:
    print(f"Title: {paper.title}")
    print(f"Authors: {', '.join(paper.authors)}")
    print(f"BibTeX Key: {paper.paper_id}")
```

### Get Raw BibTeX

```python
# Get raw BibTeX entries
bibtex_entries = searcher.search_bibtex("zero knowledge", max_results=3)
for entry in bibtex_entries:
    print(entry)
```

### Get Specific BibTeX Entry

```python
# Search for specific entries using targeted queries
papers = searcher.search("ACISP:LZXSW24", max_results=1)
if papers:
    # Access the BibTeX from the paper's extra field
    bibtex = papers[0].extra.get('bibtex', '')
    print(bibtex)

# Or get raw BibTeX entries directly
bibtex_entries = searcher.search_bibtex("ACISP:LZXSW24", max_results=1)
if bibtex_entries:
    print(bibtex_entries[0])
```

## BibTeX Entry Format

CryptoBib uses standard BibTeX format. Example entry:

```bibtex
@InProceedings{ACISP:LZXSW24,
  author =       "Fangzhou Liu and
                  Xueqi Zhu and
                  Ruozhou Xu and
                  Danping Shi and
                  Peng Wang",
  title =        "The Offline Quantum Attack Against Modular Addition Variant of {Even}-{Mansour} Cipher",
  pages =        "3--19",
  editor =       acisp24ed,
  booktitle =    acisp24name1,
  volume =       acisp24vol1,
  address =      acisp24addr,
  month =        acisp24month,
  publisher =    acisp24pub,
  series =       mylncs,
  year =         2024,
  doi =          "10.1007/978-981-97-5025-2_1",
}
```

## Implementation Details

### Search Strategy

The implementation uses streaming HTTP requests to search through the large crypto.bib file without downloading it entirely. It:

1. Makes a streaming request to the crypto.bib file
2. Parses BibTeX entries on-the-fly
3. Performs case-insensitive matching against the search query
4. Returns results as they are found up to the specified limit

### Performance Considerations

- Uses streaming to avoid memory issues with the large bibliography file
- Processes entries incrementally
- Stops searching once the maximum number of results is reached
- Implements proper brace counting for correct BibTeX entry parsing

### Limitations

- No PDF download capability (CryptoBib is a bibliography database only)
- No full-text search of paper content
- Search is limited to BibTeX field content
- Dependent on CryptoBib server availability

## Testing

Run the CryptoBib tests:

```bash
# Run all tests
pytest tests/test_cryptobib.py

# Run with verbose output
pytest tests/test_cryptobib.py -v

# Test specific functionality
python test_cryptobib.py
```

## Error Handling

The implementation includes comprehensive error handling for:

- Network connectivity issues
- Malformed BibTeX entries
- Server response errors
- Parsing failures

All errors are logged and gracefully handled, returning empty results or error messages as appropriate.
