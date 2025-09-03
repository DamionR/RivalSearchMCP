# Developer Overview

**Build and Extend RivalSearchMCP**

Welcome to the developer documentation for RivalSearchMCP. This section covers everything you need to know to contribute to the project, run it locally, and understand its architecture.

## What is RivalSearchMCP?

RivalSearchMCP is a FastMCP server that provides comprehensive web research capabilities through the Model Context Protocol (MCP). It's built with Python and designed to be extensible, performant, and reliable.

## Architecture Overview

### Core Components

- **Search Engines** - Multi-engine search with fallback capabilities
- **Content Extraction** - Advanced web scraping and content parsing
- **Analysis Tools** - Content analysis and trend detection
- **MCP Integration** - FastMCP server implementation
- **Error Handling** - Robust error recovery and fallback strategies

### Technology Stack

- **Python 3.8+** - Core runtime
- **FastMCP** - MCP server framework
- **httpx** - Async HTTP client
- **BeautifulSoup** - HTML parsing
- **selectolax** - Fast HTML parsing
- **pydantic** - Data validation

## Key Features

### Multi-Engine Search
- Google Search with advanced features
- Bing, DuckDuckGo, Yahoo fallbacks
- Configurable search parameters
- Rate limiting and error handling

### Content Extraction
- 6-tier fallback extraction system
- Multi-method content parsing
- Image and media extraction
- Structured data extraction

### Website Analysis
- Comprehensive website traversal
- Content mapping and discovery
- Multi-level link following
- Performance optimization

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Quick Start
1. Clone the repository
2. Install dependencies
3. Run the development server
4. Test with MCP clients

See the [Installation Guide](installation.md) for detailed setup instructions.

## Project Structure

```
RivalSearchMCP/
├── src/                    # Source code
│   ├── core/              # Core functionality
│   ├── tools/             # MCP tools
│   ├── schemas/           # Data models
│   └── server.py          # Main server
├── docs/                  # Documentation
├── tests/                 # Test suite
└── requirements.txt       # Dependencies
```

## Contributing

We welcome contributions! See the [Contributing Guide](contributing.md) for:

- Code style guidelines
- Testing requirements
- Pull request process
- Development workflow

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/damionrashford/RivalSearchMCP/issues)
- **Discussions**: [GitHub Discussions](https://github.com/damionrashford/RivalSearchMCP/discussions)
- **Documentation**: Check the other developer guides

## Next Steps

- [Installation Guide](installation.md) - Set up your development environment
- [API Reference](api-reference.md) - Understand the codebase
- [Contributing Guide](contributing.md) - Start contributing
