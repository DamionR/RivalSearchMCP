# Quick Start Guide

**Get Your AI Assistant Searching the Web in 5 Minutes**

This guide shows you the fastest way to connect RivalSearchMCP to your AI assistant. No technical knowledge needed!

## What You Need

- An AI assistant that supports MCP (Cursor, Claude Desktop, VS Code, etc.)
- Basic internet connection
- 5 minutes of your time

## Step 1: Choose Your AI Assistant

### For Cursor Users (Easiest)
1. **Click this button:**
   [![Add to Cursor](https://img.shields.io/badge/Add%20to%20Cursor-blue?style=for-the-badge&logo=cursor)](cursor://anysphere.cursor-deeplink/mcp/install?name=RivalSearchMCP&config=eyJ1cmwiOiJodHRwczovL1JpdmFsU2VhcmNoTUNQLmZhc3RtY3AuYXBwL21jcCJ9)

2. **Cursor will open and ask if you want to add RivalSearchMCP**
3. **Click "Yes" or "Add"**
4. **You're done!**

### For Claude Desktop
1. Open Claude Desktop
2. Go to **Settings** → **MCP Servers**
3. Click **Add Server**
4. Enter: `https://RivalSearchMCP.fastmcp.app/mcp`
5. Click **Save**
6. Restart Claude Desktop

### For VS Code
1. Open VS Code
2. Create `.vscode/mcp.json` in your workspace
3. Add this:
```json
{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}
```

## Step 2: Test Your Connection

### Simple Test
Ask your AI assistant: **"What's the latest news about artificial intelligence?"**

**Before RivalSearchMCP:** "I can't access current information"

**After RivalSearchMCP:** Your AI searches the web and gives you current articles!

### What to Look For
- Your AI should start searching the web
- It should give you current information
- It should mention sources or websites

## Step 3: Try Different Types of Searches

### Current Information
- "What's the current price of Bitcoin?"
- "What's the weather like in New York right now?"
- "What are the latest iPhone 15 reviews?"

### Research Topics
- "Research renewable energy trends in 2024"
- "Find information about machine learning applications"
- "What are the best restaurants in San Francisco?"

### Website Analysis
- "Analyze the website techcrunch.com"
- "What's on the homepage of example.com?"
- "Find contact information on company.com"

## What Your AI Can Do Now

### Search Capabilities
- **Google Search** - Find current information
- **Multi-Engine Search** - Search across multiple sources
- **Content Extraction** - Read and summarize websites
- **Trend Analysis** - Get Google Trends data

### Research Tools
- **Website Traversal** - Explore website structures
- **Content Analysis** - Analyze articles and documents
- **Comprehensive Research** - Multi-source research workflows

## Troubleshooting

### "I can't search the web"
- Make sure you clicked "Yes" when Cursor asked to add RivalSearchMCP
- Try restarting your AI assistant
- Check that the server URL is correct

### "Tool not available"
- Ask: "What tools do you have available?"
- If RivalSearchMCP isn't listed, the connection failed
- Try the connection steps again

### "Still not working"
- Use the live server URL: `https://RivalSearchMCP.fastmcp.app/mcp`
- Check your internet connection
- [Report an issue](https://github.com/rivalsearchmcp/rivalsearchmcp/issues)

## Pro Tips

### Get Better Results
- **Be specific**: "Find the latest AI news from the past week" instead of "AI news"
- **Ask for analysis**: "Search for electric car reviews and tell me which ones are best"
- **Request sources**: "Find information about climate change and include your sources"

### Combine Tools
- **Search + Analysis**: "Search for renewable energy news and analyze the trends"
- **Website + Content**: "Explore techcrunch.com and find the latest startup news"

## Next Steps

Now that your AI can search the web:

1. **Explore the features** - Try different types of searches
2. **Learn more** - Check the [User Guide](../user-guide/overview.md)
3. **See examples** - Look at [Basic Usage](../examples/basic-usage.md)
4. **Get help** - [Report issues](https://github.com/rivalsearchmcp/rivalsearchmcp/issues) if needed

## Need Help?

- **Installation issues?** Check the [Installation Guide](installation.md)
- **Not working?** [Report an issue](https://github.com/rivalsearchmcp/rivalsearchmcp/issues)
- **Want to learn more?** Check the [User Guide](../user-guide/overview.md)

---

**Ready to test?** Ask your AI assistant to search for something current!
