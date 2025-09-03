# MCP Pagination 📄

**Handling Large Result Sets with Cursor-Based Pagination**

RivalSearchMCP implements full MCP pagination support following the [MCP Pagination Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination). This allows clients to efficiently handle large result sets through cursor-based pagination.

## 🎯 Overview

MCP pagination provides a standardized way to handle large result sets by:

- **Breaking results into manageable pages**
- **Using stable cursors** for consistent navigation
- **Supporting both paginated and non-paginated flows**
- **Providing graceful error handling** for invalid cursors

## 🔧 Supported Operations

RivalSearchMCP supports pagination for the following MCP operations:

| Operation | Description | Pagination Support |
|-----------|-------------|-------------------|
| `resources/list` | List available resources | ✅ Full support |
| `resources/templates/list` | List resource templates | ✅ Full support |
| `prompts/list` | List available prompts | ✅ Full support |
| `tools/list` | List available tools | ✅ Full support |

## 🚀 Basic Usage

### Simple Pagination

```python
from src.routes.pagination import MCPPaginationManager

# Initialize pagination manager
pagination = MCPPaginationManager(default_limit=20, max_limit=100)

# Paginate a list of items
items = [f"item_{i}" for i in range(150)]
result = pagination.paginate_resources_list(items, limit=25)

print(f"Items on this page: {len(result.items)}")
print(f"Total items: {result.total_count}")
print(f"Has more pages: {result.has_more}")
print(f"Next cursor: {result.nextCursor}")
```

### Cursor-Based Navigation

```python
# First page
first_page = pagination.paginate_resources_list(items, limit=25)

# Use cursor for next page
if first_page.nextCursor:
    next_page = pagination.paginate_resources_list(
        items, 
        cursor_string=first_page.nextCursor
    )
    print(f"Next page items: {len(next_page.items)}")
```

## 📊 Pagination Response Format

All paginated responses follow the MCP specification format:

```json
{
  "items": [...],           // Array of items for current page
  "nextCursor": "string",   // Cursor for next page (null if no more pages)
  "total_count": 150,       // Total number of items available
  "has_more": true          // Boolean indicating if more pages exist
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `items` | `Array` | Items for the current page |
| `nextCursor` | `string|null` | Encoded cursor for next page |
| `total_count` | `number` | Total items across all pages |
| `has_more` | `boolean` | Whether more pages exist |

## 🔍 Cursor Structure

### Cursor Components

Each cursor contains:

```json
{
  "timestamp": "2025-09-02T17:30:00.000Z",
  "page": 2,
  "limit": 25,
  "filters": {"category": "search"},
  "sort_order": "default",
  "checksum": "a741d3809d0e7ae117b610306112eaf8"
}
```

### Cursor Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `string` | ISO timestamp of cursor creation |
| `page` | `number` | Current page number |
| `limit` | `number` | Items per page |
| `filters` | `object` | Applied filters |
| `sort_order` | `string` | Sort order applied |
| `checksum` | `string` | MD5 checksum for validation |

## ⚙️ Configuration Options

### Pagination Manager Settings

```python
pagination = MCPPaginationManager(
    default_limit=50,    # Default items per page
    max_limit=1000       # Maximum items per page
)
```

### Environment Variables

```bash
# Set pagination limits
export MCP_DEFAULT_LIMIT=50
export MCP_MAX_LIMIT=1000
export MCP_CURSOR_TIMEOUT=86400  # 24 hours in seconds
```

## 🔄 Advanced Pagination Patterns

### Filtered Pagination

```python
# Create cursor with filters
cursor = pagination.create_cursor(
    page=1,
    limit=20,
    filters={"category": "AI", "year": "2025"},
    sort_order="date_desc"
)

# Paginate with filters
result = pagination.paginate_resources_list(
    items, 
    cursor_string=cursor.to_string()
)
```

### Custom Sort Orders

```python
# Available sort orders
sort_orders = [
    "default",           # Default ordering
    "date_asc",          # Oldest first
    "date_desc",         # Newest first
    "title_asc",         # Alphabetical A-Z
    "title_desc",        # Alphabetical Z-A
    "relevance"          # Relevance score
]

cursor = pagination.create_cursor(
    page=1,
    limit=25,
    sort_order="date_desc"
)
```

## 🛡️ Error Handling

### Invalid Cursor Handling

```python
try:
    result = pagination.paginate_resources_list(
        items, 
        cursor_string="invalid_cursor"
    )
except Exception as e:
    # Fallback to first page
    result = pagination.paginate_resources_list(items)
    print(f"Invalid cursor, showing first page: {len(result.items)} items")
```

### Cursor Validation

```python
# Validate cursor before use
cursor_info = pagination.get_pagination_info(cursor_string)
if cursor_info.get("is_valid"):
    result = pagination.paginate_resources_list(items, cursor_string)
else:
    print(f"Cursor validation failed: {cursor_info.get('error')}")
```

## 📱 Client Integration Examples

### Python MCP Client

```python
from mcp import ClientSession

async with ClientSession("http://localhost:8000") as session:
    # First page
    result = await session.call_tool(
        "resources_list",
        arguments={"limit": 20}
    )
    
    # Check for next page
    if result.content.get("nextCursor"):
        next_result = await session.call_tool(
            "resources_list",
            arguments={
                "cursor": result.content["nextCursor"]
            }
        )
```

### JavaScript MCP Client

```javascript
// First page
const result = await client.callTool("resources_list", {
  limit: 20
});

// Next page if available
if (result.content.nextCursor) {
  const nextResult = await client.callTool("resources_list", {
    cursor: result.content.nextCursor
  });
}
```

## 🔧 Implementation Details

### Cursor Stability

- **Checksum-based validation** ensures cursor integrity
- **Timestamp-based expiration** (24 hours) for security
- **Deterministic encoding** for consistent behavior

### Performance Optimization

- **Efficient slicing** for large datasets
- **Minimal memory overhead** during pagination
- **Fast cursor validation** with MD5 checksums

### Security Features

- **Cursor expiration** prevents long-term access
- **Checksum validation** prevents tampering
- **Rate limiting** on cursor operations

## 🚨 Best Practices

### For Server Implementations

1. **Set reasonable limits** - Balance performance with usability
2. **Validate cursors** - Always check cursor validity before use
3. **Handle errors gracefully** - Provide fallbacks for invalid cursors
4. **Monitor performance** - Track pagination performance metrics

### For Client Implementations

1. **Cache cursors** - Store cursors for efficient navigation
2. **Handle pagination errors** - Implement retry logic for failed requests
3. **Respect rate limits** - Don't overwhelm the server with rapid requests
4. **Provide user feedback** - Show pagination status to users

## 🔗 Related Documentation

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Pagination Best Practices](../developer-guide/architecture.md)
- [Overview](overview.md)
- [Overview](overview.md)

---

**Need help with pagination?** Check our [examples](../examples/basic-usage.md) or [open an issue](https://github.com/rivalsearchmcp/rivalsearchmcp/issues) on GitHub!
