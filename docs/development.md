# Development Guide

This guide covers development setup, contribution guidelines, and architecture information for the All-in-MCP server.

## Development Setup

### Prerequisites

- Python 3.12 or higher
- UV package manager
- Git
- Text editor or IDE

### Local Development

1. **Fork and clone**:

```bash
git clone https://github.com/your-username/all-in-mcp.git
cd all-in-mcp
```

2. **Set up development environment**:

```bash
uv sync --extra dev
```

3. **Run tests**:

```bash
python -m unittest discover tests/
```

4. **Run examples**:

```bash
python examples/test_iacr_search.py
```

## Project Structure

```
all-in-mcp/
├── src/all_in_mcp/          # Main source code
│   ├── __init__.py          # Package initialization
│   ├── server.py            # MCP server implementation
│   ├── paper.py             # Paper data model
│   └── academic_platforms/  # Academic platform integrations
│       ├── __init__.py      # Platform package init
│       ├── base.py          # Abstract base class
│       └── iacr.py          # IACR implementation
├── tests/                   # Unit tests
│   ├── test_iacr.py         # IACR functionality tests
│   ├── test_mcp_server.py   # Server tests
│   └── test_server.py       # Legacy tests
├── examples/                # Example scripts
│   ├── test_iacr_search.py  # IACR demo
│   └── mcp_demo.py          # Complete demo
├── docs/                    # Documentation
│   ├── README.md            # Documentation index
│   ├── api.md               # API reference
│   ├── iacr.md              # IACR integration docs
│   └── ...                  # Other documentation
└── pyproject.toml           # Project configuration
```

## Adding New Features

### Adding a New Tool

1. **Define the tool** in `server.py`:

```python
types.Tool(
    name="your-tool-name",
    description="Tool description",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"},
        },
        "required": ["param1"],
    },
)
```

2. **Implement the handler**:

```python
elif name == "your-tool-name":
    param1 = arguments.get("param1", "")
    result = your_function(param1)
    return [types.TextContent(type="text", text=result)]
```

3. **Add tests**:

```python
def test_your_tool(self):
    async def run_test():
        result = await handle_call_tool("your-tool-name", {"param1": "test"})
        # Add assertions
    asyncio.run(run_test())
```

### Adding a New Academic Platform

1. **Create platform class** in `academic_platforms/`:

```python
from .base import PaperSource

class YourPlatformSearcher(PaperSource):
    def search(self, query: str, **kwargs) -> List[Paper]:
        # Implement search logic
        pass

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        # Implement download logic
        pass

    def read_paper(self, paper_id: str, save_path: str) -> str:
        # Implement reading logic
        pass
```

2. **Add tools to server**:

```python
# Import your searcher
from .academic_platforms.your_platform import YourPlatformSearcher

# Initialize searcher
your_searcher = YourPlatformSearcher()

# Add tools in handle_list_tools() and handle_call_tool()
```

3. **Add comprehensive tests**:

```python
class TestYourPlatformSearcher(unittest.TestCase):
    def setUp(self):
        self.searcher = YourPlatformSearcher()

    def test_search(self):
        # Test search functionality
        pass
```

## Testing Guidelines

### Test Structure

- **Unit tests**: Test individual components
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows

### Writing Tests

1. **Test naming**: Use descriptive names

```python
def test_search_returns_valid_papers(self):
def test_download_creates_file(self):
def test_invalid_paper_id_raises_error(self):
```

2. **Test organization**: Group related tests

```python
class TestIACRSearcher(unittest.TestCase):
    def setUp(self):
        self.searcher = IACRSearcher()

    def test_search_basic(self):
        # Basic search test
        pass
```

3. **Mocking external dependencies**:

```python
@patch('requests.get')
def test_search_with_mock(self, mock_get):
    mock_get.return_value.json.return_value = mock_data
    # Test with mocked response
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python tests/test_iacr.py

# Run with verbose output
python -m unittest discover tests/ -v

# Run specific test method
python -m unittest tests.test_iacr.TestIACRSearcher.test_search_basic
```

## Code Style

### Python Style Guidelines

- Follow PEP 8
- Use type hints
- Add docstrings to functions and classes
- Keep functions focused and small

### Example Function:

```python
def search_papers(query: str, max_results: int = 10) -> List[Paper]:
    """
    Search for academic papers.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of Paper objects matching the query

    Raises:
        ValueError: If query is empty
        NetworkError: If unable to reach search API
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")

    # Implementation here
    return papers
```

## Contributing

### Contribution Process

1. **Fork the repository**
2. **Create a feature branch**:

```bash
git checkout -b feature/your-feature-name
```

3. **Make changes**:

   - Add new functionality
   - Write tests
   - Update documentation

4. **Test thoroughly**:

```bash
python -m unittest discover tests/
python examples/test_iacr_search.py
```

5. **Submit pull request**:
   - Clear description of changes
   - Reference any related issues
   - Include test results

### Commit Guidelines

- Use clear, descriptive commit messages
- Keep commits focused on single changes
- Reference issues when applicable

Example commit messages:

```
feat: Add bioRxiv paper search integration
fix: Handle network timeouts in PDF download
docs: Update API documentation for new tools
test: Add comprehensive tests for IACR searcher
```

### Documentation

When adding features:

- Update API documentation
- Add usage examples
- Update relevant guides
- Include inline code comments

## Architecture

### MCP Server Architecture

The server follows the Model Context Protocol specification:

1. **Tool Registration**: Tools are registered with schemas
2. **Request Handling**: Incoming requests are routed to handlers
3. **Response Formatting**: Results are formatted as MCP responses

### Data Flow

```
Client Request → MCP Server → Tool Handler → Academic Platform → Response
```

### Error Handling Strategy

- Graceful degradation for network issues
- Clear error messages for user issues
- Logging for debugging
- Retry logic for transient failures

### Performance Considerations

- Async operations where beneficial
- Connection pooling for HTTP requests
- Caching for repeated requests
- Rate limiting for external APIs
