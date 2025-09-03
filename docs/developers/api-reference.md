# API Reference

**Core Classes, Functions, and Data Structures**

This page documents the main API components of RivalSearchMCP for developers who want to understand, extend, or integrate with the codebase.

## Core Modules

### Search Engines

#### GoogleSearchEngine
```python
class GoogleSearchEngine:
    """Primary search engine with advanced features and fallbacks."""
    
    async def search(
        self, 
        query: str, 
        num_results: int = 10,
        language: str = "en"
    ) -> List[SearchResult]
```

**Parameters:**
- `query`: Search query string
- `num_results`: Number of results to return (default: 10)
- `language`: Language code (default: "en")

**Returns:** List of SearchResult objects

#### MultiEngineSearch
```python
class MultiEngineSearch:
    """Multi-engine search with fallback capabilities."""
    
    async def search_with_fallback(
        self, 
        query: str,
        primary_engine: str = "google",
        fallback_engines: List[str] = None
    ) -> SearchResult
```

### Content Extraction

#### ContentExtractor
```python
class ContentExtractor:
    """Multi-method content extraction with fallback system."""
    
    async def extract_content(
        self, 
        url: str,
        extraction_methods: List[str] = None
    ) -> ExtractedContent
```

**Extraction Methods:**
- `beautifulsoup`: BeautifulSoup parsing
- `selectolax`: Fast HTML parsing
- `readability`: Readability algorithm
- `newspaper`: Newspaper3k extraction
- `trafilatura`: Trafilatura extraction
- `manual`: Manual text extraction

#### WebsiteTraverser
```python
class WebsiteTraverser:
    """Comprehensive website exploration and mapping."""
    
    async def traverse(
        self, 
        url: str,
        mode: str = "research",
        max_depth: int = 3
    ) -> WebsiteMap
```

**Modes:**
- `research`: Content-focused exploration
- `docs`: Documentation structure
- `map`: Site architecture mapping

### Data Models

#### SearchResult
```python
class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str
    timestamp: datetime
    relevance_score: float
```

#### ExtractedContent
```python
class ExtractedContent(BaseModel):
    title: str
    content: str
    text: str
    html: str
    metadata: Dict[str, Any]
    extraction_method: str
    confidence_score: float
```

#### WebsiteMap
```python
class WebsiteMap(BaseModel):
    root_url: str
    pages: List[PageInfo]
    structure: Dict[str, List[str]]
    metadata: Dict[str, Any]
```

## Tool Functions

### MCP Tools

#### google_search
```python
async def google_search(
    ctx: Context,
    query: str,
    num_results: int = 10
) -> str
```

**MCP Tool:** Performs Google search and returns formatted results

#### retrieve_content
```python
async def retrieve_content(
    ctx: Context,
    url: str,
    extraction_method: str = "auto"
) -> str
```

**MCP Tool:** Extracts content from URLs with multiple fallback methods

#### traverse_website
```python
async def traverse_website(
    ctx: Context,
    url: str,
    mode: str = "research"
) -> str
```

**MCP Tool:** Explores and maps website structure

## Configuration

### Environment Variables
```bash
# Debug and logging
RIVAL_SEARCH_DEBUG=true
RIVAL_SEARCH_LOG_LEVEL=DEBUG

# Performance
RIVAL_SEARCH_MAX_WORKERS=4
RIVAL_SEARCH_TIMEOUT=30

# Search settings
RIVAL_SEARCH_DEFAULT_ENGINE=google
RIVAL_SEARCH_FALLBACK_ENGINES=bing,duckduckgo,yahoo
```

### Configuration File
```python
# config.py
class Config:
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    MAX_WORKERS: int = 4
    SEARCH_TIMEOUT: int = 30
    DEFAULT_ENGINE: str = "google"
    FALLBACK_ENGINES: List[str] = ["bing", "duckduckgo", "yahoo"]
```

## Error Handling

### ErrorHandler
```python
class ErrorHandler:
    """Centralized error handling and recovery."""
    
    async def handle_error(
        self, 
        error: Exception,
        context: str,
        fallback_strategy: str = "retry"
    ) -> Any
```

**Fallback Strategies:**
- `retry`: Retry with exponential backoff
- `fallback_engine`: Use alternative search engine
- `degraded_mode`: Continue with limited functionality
- `user_notification`: Inform user of the issue

### SearchFallbackStrategy
```python
class SearchFallbackStrategy:
    """Handles search engine failures and fallbacks."""
    
    async def execute_fallback(
        self, 
        failed_engine: str,
        query: str
    ) -> SearchResult
```

## Performance Optimization

### PerformanceMonitor
```python
class PerformanceMonitor:
    """Monitors and optimizes performance."""
    
    async def measure_performance(
        self, 
        operation: str,
        start_time: float
    ) -> PerformanceMetrics
```

### LRUCache
```python
class LRUCache:
    """LRU cache for frequently accessed data."""
    
    def get(self, key: str) -> Any
    def set(self, key: str, value: Any) -> None
    def invalidate(self, key: str) -> None
```

## Testing

### Test Utilities
```python
# Test helpers for common operations
async def create_test_server() -> FastMCPServer
async def create_test_client() -> MCPClient
def create_mock_response() -> MockResponse
```

### Test Configuration
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

## Extension Points

### Custom Search Engines
```python
class CustomSearchEngine(BaseSearchEngine):
    """Implement custom search engine."""
    
    async def search(self, query: str) -> List[SearchResult]:
        # Your custom implementation
        pass
```

### Custom Extractors
```python
class CustomExtractor(BaseExtractor):
    """Implement custom content extraction."""
    
    async def extract(self, url: str) -> ExtractedContent:
        # Your custom implementation
        pass
```

## Next Steps

- [Installation Guide](installation.md) - Set up development environment
- [Contributing Guide](contributing.md) - Start contributing

