# Installation Guide

**Connect RivalSearchMCP to Your AI Assistant in Minutes**

This guide shows you exactly how to connect RivalSearchMCP to different AI assistants and applications. No technical knowledge required!

## What You're Actually Doing

When you connect RivalSearchMCP to your AI assistant, you're telling it "Hey, when I ask for current information, use this tool to search the web instead of saying you don't know."

## Option 1: Use the Live Server (Easiest - No Installation)

**This is the recommended way for most users.**

### For Cursor Users
Click this button to add RivalSearchMCP to Cursor in one click:

[![Add to Cursor](https://img.shields.io/badge/Add%20to%20Cursor-blue?style=for-the-badge&logo=cursor)](cursor://anysphere.cursor-deeplink/mcp/install?name=RivalSearchMCP&config=eyJ1cmwiOiJodHRwczovL1JpdmFsU2VhcmNoTUNQLmZhc3RtY3AuYXBwL21jcCJ9)

**What happens:**
1. Click the button
2. Cursor opens and asks if you want to add RivalSearchMCP
3. Click "Yes" or "Add"
4. Your AI assistant can now search the web!

### For Claude Desktop
1. Open Claude Desktop
2. Go to **Settings** → **MCP Servers**
3. Click **Add Server**
4. Enter this URL: `https://RivalSearchMCP.fastmcp.app/mcp`
5. Click **Save**
6. Restart Claude Desktop

### For VS Code
1. Open VS Code
2. Create or open `.vscode/mcp.json` in your workspace
3. Add this configuration:
```json
{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}
```

### For Other MCP-Compatible Apps
Add this to your MCP configuration:
```json
{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}
```

## Option 2: Install Locally (For Advanced Users)

**Only do this if you want full control or the live server doesn't work.**

### Step 1: Install Python
- **Windows**: Download from [python.org](https://python.org) - check "Add Python to PATH"
- **macOS**: Download from [python.org](https://python.org) or use `brew install python`
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### Step 2: Download RivalSearchMCP
```bash
git clone https://github.com/rivalsearchmcp/rivalsearchmcp.git
cd rivalsearchmcp
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Server
```bash
python -m src.server
```

### Step 5: Connect Your AI Assistant
Use this configuration instead of the live server URL:
```json
{
  "mcpServers": {
    "rivalsearchmcp": {
      "command": "python",
      "args": ["-m", "src.server"],
      "transport": {
        "type": "stdio"
      }
    }
  }
}
```

## Test Your Connection

### Simple Test
Ask your AI assistant: **"Search for 'latest AI news' and tell me what you find"**

**If it works:** Your AI will search the web and give you current information.

**If it doesn't work:** Your AI will say it can't access current information or doesn't know how to search.

### What You Should See
- **Before**: "I can't access current information" or "I don't know about recent events"
- **After**: Your AI searches the web and gives you current articles, news, and information

## Troubleshooting

### "Server not found" or "Connection failed"
- Make sure you're using the correct URL: `https://RivalSearchMCP.fastmcp.app/mcp`
- Check your internet connection
- Try restarting your AI assistant

### "Tool not available" or "Function not found"
- Make sure the server is connected properly
- Try asking: "What tools do you have available?"
- Restart your AI assistant

### Local installation issues
- Make sure Python is installed: `python --version`
- Make sure you're in the right directory
- Check that dependencies are installed: `pip list`

## What Your AI Can Do Now

Once connected, your AI assistant can:
- **Search the web** for current information
- **Read websites** and summarize content
- **Get latest news** and updates
- **Research topics** using multiple sources
- **Find current prices** and data
- **Analyze trends** and patterns

## Need Help?

- **Connection issues?** Try the live server first
- **Still not working?** [Report an issue](https://github.com/rivalsearchmcp/rivalsearchmcp/issues)
- **Want to learn more?** Check the [User Guide](../user-guide/overview.md)

---

**Ready to test?** Ask your AI assistant to search for something current!
