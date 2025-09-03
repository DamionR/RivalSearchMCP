# RivalSearchMCP

Advanced MCP server for web research, content discovery, and trends analysis.

## What it does

RivalSearchMCP provides comprehensive tools for accessing web content, performing Google searches, analyzing websites, conducting research workflows, and analyzing Google Trends data. It includes 6 core tool categories for comprehensive web research capabilities.

## Why it's useful

- Access web content and perform searches with anti-detection measures
- Analyze website content and structure with intelligent crawling
- Conduct end-to-end research workflows with progress tracking
- Analyze trends data with comprehensive export options
- Generate LLMs.txt documentation files for websites
- Integrate with AI assistants for enhanced web research

## How to get started

### Connect to Live Server

Add this configuration to your MCP client:

**For Cursor:**
```json
{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}
```

**For Claude Desktop:**
- Go to Settings → Add Remote Server
- Enter URL: `https://RivalSearchMCP.fastmcp.app/mcp`

**For VS Code:**
- Add the above JSON to your `.vscode/mcp.json` file

**For Claude Code:**
- Use the built-in MCP management: `claude mcp add RivalSearchMCP --url https://RivalSearchMCP.fastmcp.app/mcp`

## Available Tools

### Search & Discovery (1 tool)
- **web_search** - Advanced web search with Cloudflare bypass, rich snippets detection, and multi-engine fallback

### Content Retrieval (2 tools)
- **retrieve_content** - Enhanced content retrieval from URLs with multiple extraction methods
- **stream_content** - Real-time streaming content processing from WebSocket URLs

### Website Analysis (1 tool)
- **traverse_website** - Intelligent website exploration with different modes (research, docs, map)

### Content Analysis (2 tools)
- **analyze_content** - AI-powered content analysis and insights extraction
- **extract_links** - Link extraction and analysis from web pages

### Trends Analysis (10 tools)
- **search_trends** - Search for trends data for given keywords
- **get_related_queries** - Get related queries for a keyword with interest values
- **get_interest_by_region** - Get interest by geographic region for a keyword
- **get_trending_searches** - Get trending searches for a location
- **export_trends_to_csv** - Export trends data to CSV file
- **export_trends_to_json** - Export trends data to JSON file
- **create_sql_table** - Create SQLite table with trends data
- **compare_keywords_comprehensive** - Comprehensive comparison of multiple keywords
- **get_interest_over_time** - Get interest over time for keywords
- **get_related_topics** - Get related topics for a keyword

### Research Workflows (1 tool)
- **research_topic** - End-to-end research workflow for comprehensive topic analysis

### Documentation Generation (1 tool)
- **generate_llms_txt** - Generate LLMs.txt files for websites following the llmstxt.org specification

## Key Features

- **Anti-Detection**: Cloudflare bypass and rate limiting for reliable scraping
- **Rich Snippets**: Advanced detection of featured snippets and rich results
- **Multi-Engine Fallback**: Automatic fallback to alternative search engines
- **Progress Tracking**: Real-time progress reporting for long-running operations
- **Data Export**: Multiple format support (CSV, JSON, SQL) for trends data
- **Intelligent Crawling**: Smart website traversal with configurable depth and modes

## Documentation

📖 **[Documentation](https://damionrashford.github.io/RivalSearchMCP)** - Full documentation

**Local Documentation:**
- [User Guide](docs/user-guide/overview.md) - Complete guide to using all tools
- [Examples](docs/examples/basic-usage.md) - Real-world usage examples
- [Installation](docs/getting-started/installation.md) - Setup instructions
- [Quick Start](docs/getting-started/quick-start.md) - Get running in 5 minutes
- [Troubleshooting](docs/getting-started/troubleshooting.md) - Solve common issues

## Who maintains this project

Open source project maintained by the community. Contributions are welcome.

## License

See [LICENSE](LICENSE) file for details.