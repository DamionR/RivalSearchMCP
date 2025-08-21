# RivalSearchMCP

**Advanced MCP server** for web retrieval, search, and content discovery. Bypass restrictions, access any content, and gather comprehensive information from the web.

## 🚀 **Connect to Live Server**

**Your RivalSearchMCP server is live and ready to use!**

### **Quick Connect**
Add this configuration to your MCP client:

**For Cursor:**
```json
{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp",
      "headers": {}
    }
  }
}
```

**For Claude Desktop:**
- Go to Settings → Add Remote Server
- Enter URL: `https://RivalSearchMCP.fastmcp.app/mcp`

**For VS Code:**
- Add the above JSON to your `.vscode/mcp.json` file

### **What You Get**
- **8 Advanced Tools** for web research and content discovery
- **Bypass Any Restrictions** - Get past paywalls, bot blocks, and rate limits
- **Google Search Scraping** - Direct access with metadata extraction
- **Intelligent Content Retrieval** - Smart parsing and analysis
- **Website Traversal** - Discover and explore related content
- **Data Management** - Store and retrieve research data

## 🛠️ **Available Tools**

### **Web Retrieval**
- **`retrieve_content`** - Get content from URLs or search queries
- **`stream_content`** - Real-time streaming from WebSocket URLs

### **Search & Discovery**
- **`google_search`** - Advanced Google Search with metadata
- **`traverse_website`** - Intelligent website exploration

### **Analysis & Processing**
- **`analyze_content`** - Extract insights and key points from content
- **`research_topic`** - End-to-end research workflow

### **Data Management**
- **`store_data`** - Save research data for later use
- **`retrieve_data`** - Access stored research data

## 🏗️ **For Developers**

### **Local Installation**
If you want to run the server locally for development:

```bash
# Clone repository
git clone https://github.com/damionrashford/RivalSearchMCP.git
cd RivalSearchMCP

# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

### **Local MCP Configuration**
For local development, use this configuration:

```json
{
  "mcpServers": {
    "RivalSearchMCP": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

## 📚 **Documentation**

- **[Setup Guide](docs/setup_guide.md)** - Detailed installation and configuration
- **[API Reference](docs/api.md)** - Complete tool documentation
- **[Usage Examples](docs/usage.md)** - Real-world usage scenarios
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## 🔗 **Connect Now**

**Ready to start?** Add the Remote MCP configuration above to your client and connect to:

**`https://RivalSearchMCP.fastmcp.app/mcp`**

No installation required - just connect and start researching!