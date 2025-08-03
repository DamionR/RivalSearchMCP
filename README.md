# RivalSearchMCP

**Advanced MCP server** for web retrieval, intelligent content discovery, and data management. Bypass restrictions, access any content, and build knowledge graphs with AI-powered reasoning.

## 🚀 What You Can Do

### 🌐 **Smart Web Access**
- **Bypass Any Restrictions**: Get past paywalls, bot blocks, and rate limits
- **Google Search Integration**: Use `search:your query` to find anything
- **Intelligent Link Following**: Automatically discover related content across websites
- **Multi-Format Support**: Handle text, images (with OCR), streaming data, and more
- **Archive Fallbacks**: Access blocked content through archive services

### 🧠 **AI-Powered Research**
- **Deep Website Exploration**: Follow links intelligently to gather comprehensive information
- **Documentation Navigation**: Specialized tools for exploring technical docs and APIs
- **Competitive Analysis**: Map website structures and discover key content
- **Adaptive Reasoning**: Multi-step problem solving with branching logic

### 💾 **Knowledge Management**
- **Graph Database**: Store facts, relationships, and insights
- **Smart Search**: Find stored information quickly
- **Persistent Memory**: Keep your research across sessions
- **Structured Data**: Extract and organize information automatically

## 📦 Quick Setup

### Installation
```bash
git clone https://github.com/DamionR/RivalSearchMCP.git
cd RivalSearchMCP
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

## 🛠️ Available Tools

### 🌐 **Web Research Tools**

**`rival_retrieve`** - Your main web access tool
- Get any webpage content, bypass restrictions
- Use `search:your topic` for Google searches
- Enable `traverse_links=True` for multi-page discovery
- Perfect for: Single pages, search results, comprehensive research

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

### 🧠 **AI Processing Tools**

**`adaptive_reason`** - Smart problem solving
- Step-by-step reasoning with branching paths
- Revise and extend your thinking process
- Use for: Complex analysis, decision making, research synthesis

### 💾 **Data Management Tools**

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

*Plus 6 additional data management tools for links, facts, and advanced operations*

## 🔍 **Common Workflows**

### Research a Topic Thoroughly
```python
# 1. Start with a search to find sources
rival_retrieve(resource="search:artificial intelligence trends 2024", limit=10)

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

### Discover Content with Link Traversal
```python
# Single page with intelligent link following
rival_retrieve(
    resource="https://research-article.com",
    traverse_links=True,
    max_depth=2,
    max_pages=5,
    same_domain_only=True
)

# Cross-domain research (be careful with max_pages)
rival_retrieve(
    resource="https://starting-point.com",
    traverse_links=True,
    max_depth=1,
    max_pages=8,
    same_domain_only=False
)
```

## 🔧 **Configuration Options**

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

## 🧪 Testing & Development

```bash
# Run all tests
python -m pytest tests/ -v

# Test with MCP Inspector (interactive testing)
npx @modelcontextprotocol/inspector python src/server.py

# Test specific functionality
python -m pytest tests/test_fetch.py -v
```

## ⚙️ **Advanced Features**

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

## 🆘 **Support & Help**

### Common Issues
- **Network Errors**: Check internet connection and proxy settings
- **Empty Results**: Try different search terms or sources
- **Slow Performance**: Reduce `max_pages` or `max_depth` for faster results

### Getting Help
- **Test Interactively**: Use MCP Inspector for debugging
- **Check Logs**: Server provides detailed logging for troubleshooting
- **Validate Setup**: Ensure all dependencies are installed correctly

## 📄 **Requirements**

- **Python**: 3.8 or higher
- **Internet Access**: Required for web retrieval
- **Optional**: Tesseract for enhanced OCR functionality

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Add tests for new functionality
4. Ensure tests pass: `python -m pytest tests/ -v`
5. Submit a pull request

## 📋 **Architecture**

The server uses a **modular FastMCP architecture**:

```
src/
├── server.py              # Main server entry point
├── tools/
│   ├── web_tools.py       # Web retrieval and research tools
│   ├── reasoning_tools.py # AI processing and reasoning
│   └── data_tools.py      # Data storage and management
├── prompts.py            # Reusable prompt templates
├── resources.py          # Server information and help
└── core/                 # Core functionality modules
```

This design makes it easy to:
- **Add new tools** to specific categories
- **Maintain and update** functionality
- **Understand the codebase** quickly
- **Extend capabilities** as needed

---

**Ready to start exploring the web intelligently?** Install the server, connect it to your AI assistant, and begin discovering content like never before! 🚀