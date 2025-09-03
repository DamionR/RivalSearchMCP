# Troubleshooting Guide

**Solve Common Issues and Get RivalSearchMCP Working**

This guide helps you fix the most common problems users encounter when setting up and using RivalSearchMCP.

## Quick Fixes

### RivalSearchMCP Not Working
**Problem:** Your AI assistant says "I can't search the web" or "Tool not available"

**Quick Fix:**
1. Ask your AI: "What tools do you have available?"
2. If RivalSearchMCP isn't listed, the connection failed
3. Try reconnecting using the installation steps

### Search Not Returning Results
**Problem:** Searches work but return no results or errors

**Quick Fix:**
1. Check your internet connection
2. Try a simple search like "weather today"
3. Restart your AI assistant

## Common Issues

### Connection Problems

#### "Failed to connect to server"
**Symptoms:**
- Error message about connection failure
- AI assistant can't access RivalSearchMCP tools

**Solutions:**
1. **Check server status:**
   - Visit: `https://RivalSearchMCP.fastmcp.app/mcp`
   - Should show a response (even if it's an error page)

2. **Verify your configuration:**
   ```json
   {
     "mcpServers": {
       "RivalSearchMCP": {
         "url": "https://RivalSearchMCP.fastmcp.app/mcp"
       }
     }
   }
   ```

3. **Try restarting your AI assistant**

## Platform-Specific Issues

### Cursor Issues

#### "Add to Cursor button not working"
**Solutions:**
1. **Make sure Cursor is installed and running**
2. **Click the button again**
3. **Check Cursor's MCP settings manually**

### Claude Desktop Issues

#### "Can't find MCP settings"
**Solutions:**
1. **Go to Settings → MCP Servers**
2. **Click "Add Server"**
3. **Enter the URL manually**

## Still Having Issues?

### Get Help
- **Check the [Installation Guide](installation.md)** for detailed setup
- **Review the [User Guide](../user-guide/overview.md)** for usage tips
- **Report issues** on [GitHub](https://github.com/damionrashford/RivalSearchMCP/issues)

### Common Solutions
1. **Restart your AI assistant**
2. **Check your internet connection**
3. **Verify the server URL is correct**
4. **Try a different search query**
5. **Wait a few minutes and try again**
