# RivalSearchMCP

**Advanced MCP server** for web retrieval, intelligent content discovery, and data management. Bypass restrictions, access any content, and build knowledge graphs with AI-powered reasoning.

## What You Can Do

### Smart Web Access
- **Bypass Any Restrictions**: Get past paywalls, bot blocks, and rate limits
- **Multi-Engine Search**: Use DuckDuckGo, Startpage, Brave Search, and Searx
- **Intelligent Link Following**: Automatically discover related content across websites
- **Multi-Format Support**: Handle text, images (with OCR), streaming data, and more
- **Archive Fallbacks**: Access blocked content through archive services

### AI-Powered Research
- **Deep Website Exploration**: Follow links intelligently to gather comprehensive information
- **Documentation Navigation**: Specialized tools for exploring technical docs and APIs
- **Competitive Analysis**: Map website structures and discover key content
- **Adaptive Reasoning**: Multi-step problem solving with branching logic

### Knowledge Management
- **Graph Database**: Store facts, relationships, and insights
- **Smart Search**: Find stored information quickly
- **Persistent Memory**: Keep your research across sessions
- **Structured Data**: Extract and organize information automatically

## Quick Setup

### Installation
```bash
git clone https://github.com/DamionR/RivalSearchMCP.git
cd RivalSearchMCP
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Basic Usage
```bash
# Start for Claude Desktop (default)
python src/server.py

# Start with web interface
python src/server.py --transport http --port 8000

# Start for real-time applications
python src/server.py --transport sse --port 8001
```

### Connect to Claude Desktop
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "rival-search": {
      "command": "python",
      "args": ["/path/to/RivalSearchMCP/src/server.py"]
    }
  }
}
```

## Available Tools

### Web Research Tools

**`rival_retrieve`** - Enhanced web content retrieval
- Get any webpage content, bypass restrictions
- Use `search:your topic` for multi-engine searches
- Enable `traverse_links=True` for multi-page discovery
- Perfect for: Single pages, search results, comprehensive research

**`google_search`** - Multi-engine search
- Uses DuckDuckGo, Startpage, Brave Search, and Searx
- Privacy-focused search with fallback engines
- Use for: Finding information across multiple search engines

**`research_website`** - Deep topic exploration
- Intelligently follow related links
- Optimized for thorough content discovery
- Use for: Academic research, market analysis, comprehensive studies

**`explore_docs`** - Technical documentation specialist
- Navigate documentation sites efficiently
- Find APIs, guides, and technical references
- Use for: Learning new technologies, API documentation

**`map_website`** - Site structure analysis
- Discover key pages and site architecture
- Great for competitive analysis
- Use for: Understanding competitors, site audits

**`stream_retrieve`** - Real-time data access
- Connect to WebSocket streams and live data
- Use for: Real-time feeds, streaming APIs

**`extract_images`** - Visual content extraction
- Pull images from web pages with OCR text extraction
- Use for: Visual research, document analysis

**`batch_retrieve`** - Parallel content retrieval
- Retrieve content from multiple resources simultaneously
- Use for: Bulk data collection, comparative analysis

### AI Processing Tools

**`adaptive_reason`** - Smart problem solving
- Step-by-step reasoning with branching paths
- Revise and extend your thinking process
- Use for: Complex analysis, decision making, research synthesis

### Data Management Tools

**`add_nodes`** - Store your discoveries
- Save facts, relationships, and insights
- Build your personal knowledge graph
- Use for: Preserving research, building knowledge base

**`search_nodes`** - Find stored information
- Search through your saved research
- Quick access to previous discoveries
- Use for: Retrieving insights, building on past work

**`get_full_store`** - View your knowledge graph
- See all stored information and connections
- Export your research data
- Use for: Understanding your knowledge base, data export

**`add_links`** - Create relationships
- Connect nodes in your knowledge graph
- Build semantic relationships between concepts
- Use for: Organizing research, creating connections

**`remove_nodes`** - Clean up data
- Remove unwanted nodes from your knowledge graph
- Use for: Data cleanup, removing outdated information

**`clear_store`** - Reset knowledge graph
- Clear all stored data
- Use for: Starting fresh, clearing test data

## Common Workflows

### Research a Topic Thoroughly
```python
# 1. Start with a search to find sources
rival_retrieve(resource="search:artificial intelligence trends 2025", limit=10)

# 2. Deep dive into promising sources
research_website(url="https://promising-source.com", max_pages=8, store_data=True)

# 3. Search your stored research
search_nodes(query="key trends findings")

# 4. Use AI reasoning to analyze
adaptive_reason(step_content="Analyze the key AI trends...", ...)
```

### Explore Technical Documentation
```python
# 1. Start with the main docs page
rival_retrieve(resource="https://docs.framework.com")

# 2. Systematically explore documentation
explore_docs(url="https://docs.framework.com", max_pages=20, store_data=True)

# 3. Find specific information
search_nodes(query="API authentication examples")
```

### Analyze a Competitor
```python
# 1. Map their website structure
map_website(url="https://competitor.com", max_pages=25, store_data=True)

# 2. Research specific areas
research_website(url="https://competitor.com/products", max_pages=10, store_data=True)

# 3. Analyze findings
search_nodes(query="competitor features pricing")
```

## Configuration Options

### Transport Methods
| Transport | Best For | Command |
|-----------|----------|---------|
| **STDIO** | Claude Desktop, local AI tools | `python src/server.py` |
| **HTTP** | Web apps, remote access | `python src/server.py --transport http` |
| **SSE** | Real-time applications | `python src/server.py --transport sse` |

### Integration Examples

**With Cursor IDE:**
```json
{
  "command": "python",
  "args": ["src/server.py"],
  "cwd": "/path/to/RivalSearchMCP"
}
```

**HTTP API Usage:**
```python
import requests

response = requests.post("http://localhost:8000/mcp", json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "rival_retrieve",
        "arguments": {"resource": "https://example.com"}
    }
})
```

## Testing & Development

```bash
# Run comprehensive test suite
python tests/test_suite.py

# Test with MCP Inspector (interactive testing)
npx @modelcontextprotocol/inspector python src/server.py

# Run specific tests
python -m pytest tests/ -v
```

## Advanced Features

### Link Traversal Configuration
- **`max_depth`**: How many link levels to follow (1-3 recommended)
- **`max_pages`**: Total pages to fetch (5-20 depending on use case)
- **`same_domain_only`**: Stay within the original domain for focused research

### Bypass Capabilities
- **Paywall Detection**: Automatically detects and bypasses paywalls
- **Proxy Rotation**: Uses multiple proxy sources for reliability
- **User Agent Rotation**: Mimics different browsers and devices
- **Archive Fallbacks**: Falls back to archive services when blocked

### Data Storage
- **Graph Structure**: Stores information as interconnected nodes
- **Fact Extraction**: Automatically extracts key information
- **Relationship Mapping**: Understands connections between concepts
- **Persistent Storage**: Keeps your research between sessions

## Support & Help

### Common Issues
- **Network Errors**: Check internet connection and proxy settings
- **Empty Results**: Try different search terms or sources
- **Slow Performance**: Reduce `max_pages` or `max_depth` for faster results

### Getting Help
- **Test Interactively**: Use MCP Inspector for debugging
- **Check Logs**: Server provides detailed logging for troubleshooting
- **Validate Setup**: Ensure all dependencies are installed correctly

## Requirements

- **Python**: 3.10 or higher
- **Internet Access**: Required for web retrieval
- **Optional**: Tesseract for enhanced OCR functionality

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Add tests for new functionality
4. Ensure tests pass: `python tests/test_suite.py`
5. Submit a pull request

## Architecture

The server uses a **modular FastMCP architecture**:

```
src/
├── server.py              # Main server entry point
├── mcp_server.py          # Custom MCP server implementation
├── tools/
│   ├── web_tools.py       # Web retrieval and research tools
│   ├── reasoning_tools.py # AI processing and reasoning
│   └── data_tools.py      # Data storage and management
├── core/
│   ├── fetch.py           # Core fetching logic
│   ├── search_engines.py  # Multi-engine search implementation
│   ├── bypass.py          # Bypass techniques
│   └── traversal.py       # Link traversal logic
├── data_store/
│   └── manager.py         # Knowledge graph management
├── reasoning/
│   └── processor.py       # AI reasoning engine
├── prompts.py            # Reusable prompt templates
├── resources.py          # Server information and help
└── schemas/
    └── schemas.py        # Data models and schemas
```

This design makes it easy to:
- **Add new tools** to specific categories
- **Maintain and update** functionality
- **Understand the codebase** quickly
- **Extend capabilities** as needed

---

**Ready to start exploring the web intelligently?** Install the server, connect it to your AI assistant, and begin discovering content like never before!