# RivalSearchMCP Setup Guide

## 🚀 Quick Start

### 🌐 **Use the Live Server (Recommended)**

The easiest way to use RivalSearchMCP is to connect to the live deployment:

**URL:** `https://RivalSearchMCP.fastmcp.app/mcp`

Simply add this URL to any MCP-compatible client (Claude Desktop, Cursor IDE, VS Code, etc.) and start using advanced web research capabilities immediately.

### 🛠️ **Local Installation (Development)**

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
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python -m pytest tests/ -v
```

## 🖥️ Starting the Server

### Basic Server Startup
```bash
# For Claude Desktop (default)
python server.py

# With HTTP transport for web apps
python server.py --transport http --port 8000

# With SSE transport for real-time apps
python server.py --transport sse --port 8001

# View all options
python server.py --help
```

### Server Options
| Option | Description | Default |
|--------|-------------|---------|
| `--transport` | Protocol (stdio/http/sse) | stdio |
| `--host` | Host address | localhost |
| `--port` | HTTP port | 8000 |
| `--sse-port` | SSE port | 8001 |

## 🔌 Integration Setup

### Claude Desktop Configuration

1. **Find your config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the server configuration:**
```json
{
  "mcpServers": {
    "rival-search": {
      "command": "python",
      "args": ["/absolute/path/to/RivalSearchMCP/server.py"],
      "env": {
        "DEBUG": "false"
      }
    }
  }
}
```

3. **Restart Claude Desktop** to load the new server

### Cursor IDE Setup

1. **Open Cursor IDE settings**
2. **Navigate to MCP configuration**
3. **Add server configuration:**
```json
{
  "command": "python",
  "args": ["server.py"],
  "cwd": "/absolute/path/to/RivalSearchMCP"
}
```

### Other MCP Clients

For any MCP-compatible client:
```bash
# STDIO transport (most common)
python /path/to/RivalSearchMCP/server.py

# HTTP endpoint
http://localhost:8000/mcp

# SSE endpoint  
http://localhost:8001/sse
```

## 🧪 Testing Your Setup

### Verify Installation
```bash
# Run all tests
python -m pytest tests/ -v

# Test specific components
python -m pytest tests/test_server.py -v  # Server functionality
python -m pytest tests/test_fetch.py -v   # Web retrieval
python -m pytest tests/test_manager.py -v # Data storage
```

### Interactive Testing
```bash
# Launch MCP Inspector for interactive testing
npx @modelcontextprotocol/inspector python server.py

# Test basic functionality in inspector:
# 1. Try retrieve_content with a simple URL
# 2. Test search functionality with google_search
# 3. Test data storage with add_nodes
```

### Manual Server Test
```bash
# Start server manually
python server.py

# Should see output like:
# "RivalSearchMCP server started..."
# "Listening on stdio transport..."
```

## ⚙️ Configuration Options

### Environment Variables
Create a `.env` file in the project root:
```bash
# Logging level
DEBUG=false

# Proxy settings (optional)
HTTP_PROXY=http://proxy:port
HTTPS_PROXY=http://proxy:port

# OCR settings (optional)
TESSERACT_PATH=/usr/bin/tesseract
```

### Server Customization
The modular architecture allows easy customization:

```python
# server.py - Main server entry point
# src/tools/ - Tool categories (web, reasoning, data)
# src/prompts.py - Reusable prompt templates
# src/resources.py - Server information and help
```

### Data Storage Location
By default, data is stored in:
- **Knowledge Graph**: `data/store.json`
- **Logs**: `logs/rival_search.log`

To change storage location, modify `src/config.py`.

## 🔍 Troubleshooting Setup

### Common Issues

**Python Version Error**
```bash
# Check Python version
python --version

# Must be 3.8+, upgrade if needed
```

**Module Import Errors**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Permission Errors**
```bash
# On Unix systems, ensure Python executable has permission
chmod +x .venv/bin/python

# Or use absolute path in configuration
which python
```

**Network Connection Issues**
```bash
# Test basic connectivity
curl -I https://google.com

# Check proxy settings if behind corporate firewall
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

**Claude Desktop Not Loading Server**
- Verify JSON syntax in config file
- Use absolute paths in configuration
- Check Claude Desktop logs for error messages
- Restart Claude Desktop after config changes

### Verification Steps

1. **Server starts without errors**
   ```bash
   python server.py --help
   ```

2. **Tests pass successfully**
   ```bash
   python -m pytest tests/ -v
   ```

3. **MCP Inspector connects**
   ```bash
   npx @modelcontextprotocol/inspector python server.py
   ```

4. **Basic tool works**
   - Test `retrieve_content` with a simple URL
   - Verify response contains expected content

### Getting Additional Help

- **Check logs**: Look for error messages in console output
- **Test incrementally**: Start with basic functionality
- **Use MCP Inspector**: Interactive testing helps identify issues
- **Verify dependencies**: Ensure all required packages are installed

## 🚀 Next Steps

Once setup is complete:

1. **Read the Usage Guide**: Learn common workflows and patterns
2. **Try the Examples**: Start with simple retrieval operations
3. **Explore Link Traversal**: Test intelligent content discovery
4. **Build Knowledge Graphs**: Store and organize your research

Your RivalSearchMCP server is now ready to enhance your AI assistant with powerful web research capabilities!