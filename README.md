# RivalSearchMCP

Advanced MCP server for web retrieval, search, and content discovery.

## What it does

RivalSearchMCP provides tools for accessing web content, performing Google searches, analyzing websites, and conducting research workflows. It includes 6 tools for comprehensive web research capabilities.

## Why it's useful

- Access web content and perform searches
- Analyze website content and structure  
- Conduct end-to-end research workflows
- Integrate with AI assistants for enhanced web research

## How to get started

### Connect to Live Server (Recommended)

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

### Local Installation (For Developers)

```bash
# Clone repository
git clone https://github.com/damionrashford/RivalSearchMCP.git
cd RivalSearchMCP

# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

## Available Tools

- **retrieve_content** - Enhanced content retrieval with support for single/multiple resources and image extraction
- **stream_content** - Retrieve streaming content from WebSocket URLs
- **google_search** - Comprehensive Google Search with multi-engine fallback and advanced features
- **traverse_website** - Comprehensive website traversal with different modes (research, docs, map)
- **analyze_content** - Analyze content and extract insights
- **research_topic** - End-to-end research workflow for a topic

## Who maintains this project

Open source project maintained by the community. Contributions are welcome.

## License

See [LICENSE](LICENSE) file for details.