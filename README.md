# RivalSearchMCP

Advanced MCP server for web retrieval, search, and content discovery.

## What it does

RivalSearchMCP provides tools for accessing web content, performing Google searches, analyzing websites, and managing research data. It includes 8 tools for comprehensive web research capabilities.

## Why it's useful

- Access web content and perform searches
- Analyze website content and structure  
- Manage research data and findings
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

- **retrieve_content** - Get content from URLs or search queries
- **stream_content** - Real-time streaming from WebSocket URLs
- **google_search** - Advanced Google Search with metadata
- **traverse_website** - Intelligent website exploration
- **analyze_content** - Extract insights and key points from content
- **research_topic** - End-to-end research workflow
- **store_data** - Save research data for later use
- **retrieve_data** - Access stored research data

## Where to get help

- [Setup Guide](docs/setup_guide.md) - Detailed installation and configuration
- [API Reference](docs/api.md) - Complete tool documentation
- [Usage Examples](docs/usage.md) - Real-world usage scenarios
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## Who maintains this project

Open source project maintained by the community. Contributions are welcome.

## License

See [LICENSE](LICENSE) file for details.