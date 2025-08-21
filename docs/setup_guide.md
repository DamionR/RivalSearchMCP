# RivalSearchMCP Setup Guide

## 🚀 **Quick Start - Connect to Live Server**

### **Remote MCP Configuration**

The easiest way to use RivalSearchMCP is to connect to the live deployment. Add this configuration to your MCP client:

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

**For Claude Code:**
- Use the built-in MCP management: `claude mcp add RivalSearchMCP --url https://RivalSearchMCP.fastmcp.app/mcp`

### **What You Get**
- **8 Advanced Tools** for web research and content discovery
- **Bypass Any Restrictions** - Get past paywalls, bot blocks, and rate limits
- **Google Search Scraping** - Direct access with metadata extraction
- **Intelligent Content Retrieval** - Smart parsing and analysis
- **Website Traversal** - Discover and explore related content
- **Data Management** - Store and retrieve research data

## 🛠️ **Local Installation (For Developers)**

If you want to run the server locally for development or customization:

### Prerequisites
- **Python**: 3.8+ (recommended 3.12 for optimal performance)
- **Virtual Environment**: venv, conda, or poetry
- **Network**: Internet access for web retrieval
- **Optional**: Tesseract OCR for image text extraction

### Installation
```bash
# 1. Clone repository
git clone https://github.com/damionrashford/RivalSearchMCP.git
cd RivalSearchMCP

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
python server.py
```

### **Local MCP Configuration**

For local development, use this configuration:

**For Cursor:**
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

**For Claude Desktop:**
```json
{
  "mcpServers": {
    "RivalSearchMCP": {
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
        "server.py"
      ]
    }
  }
}
```

**For VS Code:**
```json
{
  "mcpServers": {
    "RivalSearchMCP": {
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
        "server.py"
      ]
    }
  }
}
```

### **FastMCP CLI Installation (Recommended for Local)**

The easiest way to install locally is using FastMCP's CLI:

```bash
# For Cursor
fastmcp install cursor server.py

# For Claude Desktop
fastmcp install claude-desktop server.py

# For Claude Code
fastmcp install claude-code server.py

# Generate MCP JSON config
fastmcp install mcp-json server.py --name "RivalSearchMCP"
```

## 🔧 **Configuration Options**

### **Environment Variables**
If your server needs environment variables:

```bash
# With FastMCP CLI
fastmcp install cursor server.py --env DEBUG=true --env API_KEY=your-key

# Or load from .env file
fastmcp install cursor server.py --env-file .env
```

### **Python Version Control**
```bash
# Use specific Python version
fastmcp install cursor server.py --python 3.11

# Run within project directory
fastmcp install cursor server.py --project /path/to/project
```

## 🎯 **Verification**

After configuration, you should see:
- **Cursor**: MCP tools available in AI assistant
- **Claude Desktop**: Hammer icon (🔨) in bottom left of input box
- **Claude Code**: Tools available in Claude's interface
- **VS Code**: MCP tools accessible in workspace

## 📋 **Requirements**

### **For Local Installation**
- **uv**: Required for FastMCP CLI installations
  ```bash
  # macOS
  brew install uv
  
  # Linux/Windows
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Python 3.11+**: Required for all installations
- **Dependencies**: Automatically handled by FastMCP CLI or manually installed

### **For Remote Connection**
- **No installation required** - just add the configuration and connect!

## 🚀 **Ready to Start**

**For most users:** Use the Remote MCP configuration at the top - no installation needed!

**For developers:** Use the local installation instructions above for development and customization.

Connect to: **`https://RivalSearchMCP.fastmcp.app/mcp`**