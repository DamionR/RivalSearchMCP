# MCP Inspector Testing Guide

Complete guide for testing RivalSearchMCP with the MCP Inspector tool.

## 🔍 What is MCP Inspector?

MCP Inspector is the official debugging and testing tool for Model Context Protocol (MCP) servers. It provides both a web UI and CLI interface for comprehensive server testing.

### Key Features
- **Interactive Web UI**: Visual tool testing and debugging
- **CLI Mode**: Automated testing and scripting
- **Multiple Transports**: Support for STDIO, HTTP, and SSE
- **Real-time Monitoring**: Live request/response inspection
- **Configuration Export**: Generate client configurations

## 🚀 Quick Start

### Testing Remote MCP Server (Recommended)
```bash
# Test the live server directly
npx @modelcontextprotocol/inspector --url https://RivalSearchMCP.fastmcp.app/mcp
```

This command will:
1. Download and run MCP Inspector (if not cached)
2. Connect to the live RivalSearchMCP server
3. Launch web UI at `http://localhost:6274`
4. Generate a secure session token
5. Automatically open your browser with authentication

### Testing Local Server
```bash
# Start with your local FastMCP server
npx @modelcontextprotocol/inspector python server.py
```

This command will:
1. Download and run MCP Inspector (if not cached)
2. Start your local RivalSearchMCP server with STDIO transport
3. Launch web UI at `http://localhost:6274`
4. Generate a secure session token
5. Automatically open your browser with authentication

### Expected Output
```
Starting MCP inspector...
⚙️ Proxy server listening on localhost:6277
🔑 Session token: abc123...
🔗 Open inspector with token pre-filled:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=abc123...
```

## 🛠️ Testing Different Transports

### 1. STDIO Transport (Default)
```bash
# Most reliable for local development
npx @modelcontextprotocol/inspector python server.py

# With environment variables
npx @modelcontextprotocol/inspector -e DEBUG=true python server.py

# With custom arguments
npx @modelcontextprotocol/inspector python server.py --custom-arg value
```

**Best for**: Local development, Claude Desktop integration testing

### 2. HTTP Transport Testing
```bash
# Terminal 1: Start HTTP server
python server.py --transport http --port 8000

# Terminal 2: Open Inspector with HTTP configuration
# Navigate to: http://localhost:6274/?transport=streamable-http&serverUrl=http://localhost:8000
```

**Best for**: Web integration testing, remote server testing

### 3. SSE Transport Testing
```bash
# Terminal 1: Start SSE server
python server.py --transport sse --port 8001

# Terminal 2: Configure Inspector for SSE
# Navigate to: http://localhost:6274/?transport=sse&serverUrl=http://localhost:8001/sse
```

**Best for**: Real-time application testing (note: SSE is deprecated)

## 🧪 Comprehensive Testing Checklist

### 1. Initial Connection Verification
- [ ] Inspector shows "Connected" status
- [ ] Server name appears as "rival-search"
- [ ] All 12 tools are visible in Tools tab
- [ ] No connection errors in console

### 2. Core Tool Testing

#### Web Retrieval Tools
```bash
# Test retrieve_content with URL
resource: "https://httpbin.org/json"
max_length: 1000
raw: false

# Test retrieve_content with search
resource: "search:FastMCP Python"
limit: 5

# Test stream_content
url: "wss://echo.websocket.org"
```

#### Reasoning Tools
```bash
# Test adaptive_reason
step_content: "Define the problem: What is 2+2?"
step_num: 1
estimated_steps: 3
continue_reasoning: true
```

#### Data Store Tools
```bash
# Test add_nodes
nodes: [{"name": "test_node", "type": "test", "facts": ["test fact"]}]

# Test search_nodes
query: "test"

# Test get_full_store
# (no parameters required)
```

### 3. Structured Output Validation
- [ ] Responses display as formatted objects (not JSON strings)
- [ ] Required fields are present in responses
- [ ] Data types match schema definitions
- [ ] Error responses follow MCP format

### 4. Error Handling Tests
- [ ] Invalid tool names return proper errors
- [ ] Missing required parameters are caught
- [ ] Invalid parameter types are rejected
- [ ] Network timeouts are handled gracefully

### 5. Performance Testing
- [ ] Tools execute within reasonable time limits
- [ ] Large responses are handled properly
- [ ] Concurrent requests work correctly
- [ ] Memory usage remains stable

## 🖥️ CLI Mode Testing

### Basic CLI Commands
```bash
# List all available tools
npx @modelcontextprotocol/inspector --cli python src/server.py --method tools/list

# Test rival_retrieve tool
npx @modelcontextprotocol/inspector --cli python src/server.py \
  --method tools/call \
  --tool-name rival_retrieve \
  --tool-arg resource="https://httpbin.org/json" \
  --tool-arg max_length=500

# Test data store operations
npx @modelcontextprotocol/inspector --cli python src/server.py \
  --method tools/call \
  --tool-name add_nodes \
  --tool-arg nodes='[{"name": "cli_test", "type": "test"}]'
```

### Automated Testing Script
```bash
#!/bin/bash
# comprehensive_cli_test.sh

echo "🔧 Testing Tools List"
npx @modelcontextprotocol/inspector --cli python src/server.py --method tools/list

echo "🔧 Testing Web Retrieval"
npx @modelcontextprotocol/inspector --cli python src/server.py \
  --method tools/call \
  --tool-name rival_retrieve \
  --tool-arg resource="https://httpbin.org/json"

echo "🔧 Testing Search"
npx @modelcontextprotocol/inspector --cli python src/server.py \
  --method tools/call \
  --tool-name rival_retrieve \
  --tool-arg resource="search:MCP protocol"

echo "🔧 Testing Data Store"
npx @modelcontextprotocol/inspector --cli python src/server.py \
  --method tools/call \
  --tool-name get_full_store

echo "✅ CLI Testing Complete"
```

## 🎯 What to Look For

### Successful Tool Execution
- **Status**: Green checkmark or success indicator
- **Response Time**: Under 30 seconds for most operations
- **Content**: Properly formatted structured output
- **No Errors**: Clean response without exception traces

### Structured Output Format
```json
{
  "success": true,
  "data": {
    "content": "Retrieved content here...",
    "url": "https://example.com"
  },
  "truncated": false,
  "remaining_bytes": 0,
  "original_url": "https://example.com",
  "is_search": false
}
```

### Common Issues and Solutions

#### Connection Failures
```bash
# Issue: "Failed to connect to MCP server"
# Solution: Use absolute paths
npx @modelcontextprotocol/inspector python /full/path/to/src/server.py

# Issue: Import errors
# Solution: Check Python environment
which python
python -c "from src.server import mcp; print('OK')"
```

#### Timeout Issues
```bash
# Issue: CLI commands timeout
# Solution: Increase timeout or use UI mode
# The UI is more reliable for interactive testing
```

#### Tool Execution Errors
- **Check parameter types**: Ensure strings are quoted, numbers are unquoted
- **Verify required parameters**: All required fields must be provided
- **Check server logs**: Look for error messages in server output

## 📊 Validation Criteria

### Connection Health
- [ ] Server connects without errors
- [ ] Authentication works (if enabled)
- [ ] Tools list loads completely
- [ ] UI remains responsive

### Tool Functionality
- [ ] **rival_retrieve**: Successfully fetches web content
- [ ] **search functionality**: Returns search results
- [ ] **adaptive_reason**: Processes reasoning steps
- [ ] **data store**: CRUD operations work correctly
- [ ] **stream_retrieve**: Handles WebSocket connections

### Data Integrity
- [ ] Structured outputs match Pydantic schemas
- [ ] Search results contain title, link, snippet
- [ ] Web content includes URL and content
- [ ] Data store operations persist correctly
- [ ] Error messages are informative

### Performance Benchmarks
- [ ] Tool listing: < 2 seconds
- [ ] Web retrieval: < 30 seconds
- [ ] Search queries: < 15 seconds
- [ ] Data operations: < 5 seconds
- [ ] Memory usage: < 500MB baseline

## 🔧 Configuration Export

### Server Entry Export
After successful testing, use the Inspector's export feature:

1. Click "Server Entry" button in Inspector UI
2. Copy the configuration to clipboard
3. Use in Claude Desktop config:

```json
{
  "command": "python",
  "args": ["/path/to/rival_search_mcp/src/server.py"],
  "env": {
    "DEBUG": "false"
  }
}
```

### Complete Servers File
Use "Servers File" button for complete configuration:

```json
{
  "mcpServers": {
    "rival-search": {
      "command": "python",
      "args": ["/path/to/rival_search_mcp/src/server.py"],
      "env": {
        "DATA_STORE_PATH": "./data_store.json"
      }
    }
  }
}
```

## 🚀 Advanced Testing Scenarios

### Environment Variable Testing
```bash
# Test with different configurations
npx @modelcontextprotocol/inspector \
  -e DEBUG=true \
  -e DATA_STORE_PATH="/tmp/test_store.json" \
  python src/server.py
```

### Load Testing
```bash
# Multiple concurrent tool calls (CLI)
for i in {1..10}; do
  npx @modelcontextprotocol/inspector --cli python src/server.py \
    --method tools/call \
    --tool-name get_full_store &
done
wait
```

### Network Simulation
```bash
# Test with network delays (requires network simulation tools)
# Or test with slow remote URLs
npx @modelcontextprotocol/inspector python src/server.py
# Then test with slow-loading websites
```

## 📝 Testing Report Template

### Test Execution Summary
- **Date**: [Test Date]
- **Environment**: [OS, Python Version]
- **Transport**: [STDIO/HTTP/SSE]
- **Tools Tested**: [12/12]
- **Success Rate**: [X%]

### Detailed Results
| Tool | Status | Response Time | Notes |
|------|--------|---------------|--------|
| rival_retrieve | ✅ | 2.3s | Web content retrieved successfully |
| search function | ✅ | 1.8s | Google search results returned |
| adaptive_reason | ✅ | 0.5s | Reasoning step processed |
| data store ops | ✅ | 0.3s | CRUD operations working |
| ... | ... | ... | ... |

### Issues Found
- [ ] None / [Description of any issues]

### Recommendations
- [ ] Ready for production use
- [ ] Needs additional testing
- [ ] Configuration adjustments needed

## 🎉 Success Criteria

Your RivalSearchMCP server is ready for production when:

- ✅ All 12 tools execute without errors
- ✅ Structured outputs display correctly in Inspector
- ✅ Web retrieval and search functionality work
- ✅ Data store operations persist correctly
- ✅ Error handling is graceful and informative
- ✅ Performance meets acceptable benchmarks
- ✅ Configuration can be exported for client use

## 🆘 Troubleshooting Tips

### Common CLI Issues
- Use absolute paths for server script
- Ensure virtual environment is activated
- Check Python version compatibility
- Verify all dependencies are installed

### UI Interface Issues
- Clear browser cache if UI doesn't load
- Check that session token is valid
- Verify no firewall blocking localhost connections
- Try different browser if issues persist

### Server-Side Issues
- Check server logs for error messages
- Verify data store file permissions
- Ensure network connectivity for web requests
- Monitor memory and CPU usage

Your FastMCP server should now be thoroughly tested and ready for integration with any MCP-compatible client!