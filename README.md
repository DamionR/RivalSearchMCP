# RivalSearchMCP

**Advanced MCP server** for web retrieval, search, and content discovery. Bypass restrictions, access any content, and gather comprehensive information from the web.

## 🚀 **Live Deployment**

**Your RivalSearchMCP server is now live and ready to use!**

Connect to the live server at: **`https://RivalSearchMCP.fastmcp.app/mcp`**

Simply add this URL to any MCP-compatible client (Claude Desktop, Cursor IDE, VS Code, etc.) and start using advanced web research capabilities immediately.

## What You Can Do

### Smart Web Access
- **Bypass Any Restrictions**: Get past paywalls, bot blocks, and rate limits
- **Google Search Scraping**: Direct Google Search with advanced features and metadata extraction
- **Intelligent Link Following**: Automatically discover related content across websites
- **Multi-Format Support**: Handle text, images (with OCR), streaming data, and more
- **Archive Fallbacks**: Access blocked content through archive services
- **Clean Content Processing**: Automatic HTML cleaning and markdown formatting
- **Single-Line Optimization**: Efficient token usage with delimited content

### Advanced Web Research
- **Deep Website Exploration**: Follow links intelligently to gather comprehensive information
- **Documentation Navigation**: Specialized tools for exploring technical docs and APIs
- **Competitive Analysis**: Map website structures and discover key content
- **Batch Processing**: Retrieve content from multiple sources simultaneously

## Quick Setup

### 🌐 **Use the Live Server (Recommended)**

The easiest way to use RivalSearchMCP is to connect to the live deployment:

**URL:** `https://RivalSearchMCP.fastmcp.app/mcp`

Add this URL to your MCP client configuration and you're ready to go!

### 🛠️ **Local Installation (Development)**

If you want to run the server locally for development or customization:

```bash
git clone https://github.com/damionrashford/RivalSearchMCP.git
cd RivalSearchMCP
python -m venv .venv-py313
source .venv-py313/bin/activate  # On Windows: .venv-py313\Scripts\activate
pip install -r requirements.txt
```

### Basic Usage
```bash
# Start the MCP server locally
python server.py
```

## Installation for Different MCP Clients

### 🚀 **FastMCP CLI (Recommended - Easiest)**

The easiest way to install RivalSearchMCP in any client is using FastMCP's first-class integrations:

#### **For Cursor IDE:**
```bash
# Navigate to your RivalSearchMCP directory
cd /path/to/RivalSearchMCP

# Install with FastMCP CLI (automatically handles dependencies)
fastmcp install cursor server.py

# Or install to workspace only
fastmcp install cursor server.py --workspace .
```

#### **For Claude Desktop:**
```bash
# Navigate to your RivalSearchMCP directory
cd /path/to/RivalSearchMCP

# Install with FastMCP CLI
fastmcp install claude-desktop server.py

# Restart Claude Desktop after installation
```

#### **For Claude Code:**
```bash
# Navigate to your RivalSearchMCP directory
cd /path/to/RivalSearchMCP

# Install with FastMCP CLI
fastmcp install claude-code server.py
```

#### **For Any MCP Client (Generate JSON Config):**
```bash
# Generate standard MCP JSON configuration
fastmcp install mcp-json server.py --name "RivalSearchMCP"

# Copy to clipboard for easy pasting
fastmcp install mcp-json server.py --name "RivalSearchMCP" --copy
```

### 🔧 **Manual Configuration (Advanced Users)**

#### **For Cursor IDE:**
Add to your `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "rival-search-mcp": {
      "command": "/path/to/RivalSearchMCP/.venv-py313/bin/python",
      "args": ["server.py"]
    }
  }
}
```

#### **For Claude Desktop:**
Add to your `~/.claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "rival-search-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "--with", "httpx",
        "--with", "cloudscraper",
        "--with", "beautifulsoup4",
        "--with", "lxml",
        "--with", "pillow",
        "--with", "websockets",
        "--with", "pytesseract",
        "--with", "fake-useragent",
        "--with", "selenium",
        "fastmcp",
        "run",
        "/path/to/RivalSearchMCP/server.py"
      ]
    }
  }
}
```

#### **For VS Code:**
Add to your workspace `.vscode/mcp.json`:
```json
{
  "mcpServers": {
    "rival-search-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "--with", "httpx",
        "--with", "cloudscraper",
        "--with", "beautifulsoup4",
        "--with", "lxml",
        "--with", "pillow",
        "--with", "websockets",
        "--with", "pytesseract",
        "--with", "fake-useragent",
        "--with", "selenium",
        "fastmcp",
        "run",
        "/path/to/RivalSearchMCP/server.py"
      ]
    }
  }
}
```

### 📋 **Requirements**

- **uv**: Must be installed for FastMCP CLI installations
  ```bash
  # macOS
  brew install uv
  
  # Linux/Windows
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **Python 3.11+**: Required for all installations
- **Dependencies**: Automatically handled by FastMCP CLI or manually installed

### 🔄 **Environment Variables (Optional)**

If you need to set environment variables:

```bash
# With FastMCP CLI
fastmcp install cursor server.py --env DEBUG=true --env API_KEY=your-key

# Or load from .env file
fastmcp install cursor server.py --env-file .env
```

### 🎯 **Verification**

After installation, you should see:
- **Cursor**: MCP tools available in AI assistant
- **Claude Desktop**: Hammer icon (🔨) in bottom left of input box
- **Claude Code**: Tools available in Claude's interface
- **VS Code**: MCP tools accessible in workspace

## Available Tools (8 Total)

### Content Retrieval Tools (2)

**`retrieve_content`** - Comprehensive content retrieval
- Get any webpage content, bypass restrictions
- Support for single URLs, multiple URLs, or search queries
- Built-in image extraction with OCR
- Clean HTML-free content with markdown formatting
- Perfect for: Single pages, batch retrieval, search results, comprehensive research

**`stream_content`** - Real-time data access
- Connect to WebSocket streams and live data
- Clean, formatted streaming content
- Use for: Real-time feeds, streaming APIs, live data monitoring

### Search Tools (1)

**`google_search`** - Comprehensive Google Search with fallback
- Direct Google Search scraping with advanced features
- Rich snippets, traffic estimation, and search features detection
- Cloudflare bypass and anti-detection measures
- Automatic fallback to multi-engine search if direct scraping fails
- Use for: High-quality Google Search results with detailed metadata

### Website Traversal Tools (1)

**`traverse_website`** - Comprehensive website exploration
- Multiple modes: research, docs, map
- Research mode: General content exploration
- Docs mode: Documentation-specific navigation
- Map mode: Website structure mapping
- Clean, formatted content from all pages
- Use for: Academic research, competitive analysis, documentation exploration

### Analysis Tools (2)

**`analyze_content`** - Content analysis and insights
- Multiple analysis types: general, sentiment, technical, business
- Key point extraction and summarization
- Sentiment analysis with scoring
- Technical term extraction
- Business metrics identification
- Use for: Content analysis, sentiment analysis, technical documentation review

**`research_topic`** - End-to-end research workflow
- Complete research pipeline from search to analysis
- Automatic source discovery and content retrieval
- Key findings extraction and synthesis
- Research recommendations and insights
- Use for: Comprehensive research projects, market analysis, academic studies

### Data Management Tools (2)

**`add_nodes`** - Add data to knowledge graph
- Store structured information for later retrieval
- Support for various data types and relationships
- Use for: Building knowledge bases, storing research findings

**`get_nodes`** - Retrieve data from knowledge graph
- Query stored information with flexible filters
- Retrieve related data and connections
- Use for: Accessing stored research, building on previous findings

## Available Prompts (8 Total)

Each tool has a corresponding prompt for optimal usage:

1. **`retrieve_content_prompt`** - Comprehensive content retrieval guidance
2. **`stream_content_prompt`** - Real-time streaming content guidance
3. **`google_search_prompt`** - Comprehensive search analysis guidance
4. **`traverse_website_prompt`** - Website exploration guidance
5. **`analyze_content_prompt`** - Content analysis guidance
6. **`research_topic_prompt`** - End-to-end research guidance
7. **`add_nodes_prompt`** - Data storage guidance
8. **`get_nodes_prompt`** - Data retrieval guidance

## Advanced Configuration

### Transport Methods
| Transport | Best For | Command |
|-----------|----------|---------|
| **STDIO** | Local AI tools, MCP clients | `python server.py` |
| **HTTP** | Web apps, remote access | `python server.py --transport http` |
| **SSE** | Real-time applications | `python server.py --transport sse` |

### HTTP API Usage
```python
import requests

response = requests.post("http://localhost:8000/mcp", json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "retrieve_content",
        "arguments": {"resource": "https://example.com"}
    }
})
```

## Testing & Development

```bash
# Run tests
python -m pytest tests/ -v

# Test with MCP Inspector (interactive testing)
npx @modelcontextprotocol/inspector python server.py

# Run linting
ruff check src/

# Auto-fix code issues
ruff check --fix src/
```

## Advanced Features

### Google Search Features
- **Direct Scraping**: Uses your exact working Google Search scraper
- **Rich Snippets Detection**: Identifies featured snippets, knowledge panels, etc.
- **Traffic Estimation**: Estimates search result traffic based on position
- **Search Features**: Detects video results, news, site links, etc.
- **Multi-Engine Fallback**: Falls back to other search engines if Google is blocked
- **Advanced Metadata**: Comprehensive search result analysis

### Link Traversal Configuration
- **`max_depth`**: How many link levels to follow (1-3 recommended)
- **`max_pages`**: Total pages to fetch (5-20 depending on use case)
- **`same_domain_only`**: Stay within the original domain for focused research

### Bypass Capabilities
- **Paywall Detection**: Automatically detects and bypasses paywalls
- **Proxy Rotation**: Uses multiple proxy sources for reliability
- **User Agent Rotation**: Mimics different browsers and devices
- **Archive Fallbacks**: Falls back to archive services when blocked
- **Cloudflare Bypass**: Advanced anti-bot protection bypass

### Content Processing
- **HTML Cleaning**: Remove scripts, ads, navigation, and unwanted elements
- **Markdown Conversion**: Convert HTML to clean, readable markdown
- **Single-Line Formatting**: Optimize content for efficient token usage
- **OCR Integration**: Extract text from images using Tesseract
- **Structured Extraction**: Extract titles, descriptions, and main content
- **Search Result Formatting**: Clean, consistent search result presentation

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

- **Python**: 3.12 or higher
- **Internet Access**: Required for web retrieval
- **Tesseract**: For enhanced OCR functionality (optional but recommended)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Add tests for new functionality
4. Ensure tests pass: `python -m pytest tests/`
5. Submit a pull request

---

**Ready to start exploring the web intelligently?** Connect to the live server at `https://RivalSearchMCP.fastmcp.app/mcp` or install locally for development!