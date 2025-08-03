# Link Traversal Guide

## 🔗 Advanced Content Discovery with Link Traversal

RivalSearchMCP includes powerful link traversal functionality, allowing you to discover and extract comprehensive information by intelligently following links across websites.

## 🚀 Quick Start

### Basic Link Traversal
```python
# Enable link traversal on rival_retrieve
rival_retrieve(
    resource="https://example.com/article",
    traverse_links=True,
    max_depth=2,
    max_pages=5
)
```

### Specialized Traversal Tools
```python
# Research a topic comprehensively
research_website(
    url="https://site.com/topic",
    max_pages=5,
    store_data=True
)

# Explore documentation sites
explore_docs(
    url="https://docs.example.com",
    max_pages=15
)

# Map website structure
map_website(
    url="https://company.com",
    max_pages=20
)
```

## 🛠️ Available Tools

### 1. `rival_retrieve` (Enhanced)
The core retrieval tool now supports link traversal for deep content discovery.

**New Parameters:**
- `traverse_links` (bool): Enable link traversal mode
- `max_depth` (int): Maximum traversal depth (default: 2)
- `max_pages` (int): Maximum pages to fetch (default: 10)
- `same_domain_only` (bool): Only follow same-domain links (default: True)

**Example Usage:**
```python
# Basic web page with link traversal
rival_retrieve(
    resource="https://techblog.com/ai-article",
    traverse_links=True,
    max_depth=2,
    max_pages=8,
    same_domain_only=True,
    store_data=True
)

# Research with external links
rival_retrieve(
    resource="https://research-hub.com/topic",
    traverse_links=True,
    max_depth=1,
    max_pages=5,
    same_domain_only=False
)
```

### 2. `research_website`
Optimized for research workflows with intelligent link filtering.

**Features:**
- Excludes common non-content pages (tags, categories, search)
- Filters out binary files (PDFs, docs)
- Prioritizes content-rich pages
- Perfect for topic research

**Example:**
```python
research_website(
    url="https://blog.openai.com/gpt-4",
    max_pages=8,
    store_data=True
)
```

**What it discovers:**
- Main article content
- Related posts and articles
- Author pages with relevant content
- Topic-specific landing pages

### 3. `explore_docs`
Designed specifically for documentation sites and technical resources.

**Features:**
- Focuses on documentation patterns (/docs/, /api/, /guide/)
- Excludes forums, blogs, and marketing pages
- Follows reference and tutorial links
- Ideal for API documentation and technical guides

**Example:**
```python
explore_docs(
    url="https://docs.fastapi.tiangolo.com",
    max_pages=20
)
```

**What it discovers:**
- API reference pages
- Tutorial and guide sections
- Code examples and samples
- Installation and setup docs

### 4. `map_website`
Maps the overall structure and key pages of a website.

**Features:**
- Broad site exploration
- Excludes utility pages (login, search, cart)
- Discovers main navigation structure
- Perfect for site audits and content mapping

**Example:**
```python
map_website(
    url="https://company.com",
    max_pages=25,
    store_data=True
)
```

**What it discovers:**
- Homepage and main sections
- Product/service pages
- About and company pages
- Key landing pages

## 📊 Structured Output Format

All traversal tools return structured `TraversalResult` objects:

```python
{
    "start_url": "https://example.com",
    "pages_fetched": 5,
    "total_attempts": 6,
    "unique_links_found": 23,
    "max_depth_reached": 2,
    "pages": [
        {
            "url": "https://example.com",
            "title": "Homepage Title",
            "content": "Page content...",
            "depth": 0
        },
        {
            "url": "https://example.com/about",
            "title": "About Us",
            "content": "About page content...",
            "depth": 1
        }
    ],
    "summary": "Traversed 5 pages starting from https://example.com",
    "config": {
        "max_depth": 2,
        "max_pages": 10,
        "same_domain_only": true
    }
}
```

## 🎯 Use Cases

### 1. **Research & Analysis**
```python
# Research a complex topic across multiple pages
research_website(
    url="https://ai-safety.com/alignment",
    max_pages=10,
    store_data=True
)

# Then query the stored data
search_nodes(query="alignment research")
```

### 2. **Documentation Discovery**
```python
# Explore new framework documentation
explore_docs(
    url="https://docs.newframework.dev",
    max_pages=20
)

# Get comprehensive understanding of API
rival_retrieve(
    resource="https://api-docs.service.com",
    traverse_links=True,
    max_depth=3,
    max_pages=15
)
```

### 3. **Competitive Analysis**
```python
# Map competitor website structure
map_website(
    url="https://competitor.com",
    max_pages=30,
    store_data=True
)

# Research their product pages
research_website(
    url="https://competitor.com/products",
    max_pages=15
)
```

### 4. **Content Aggregation**
```python
# Gather comprehensive content on a topic
rival_retrieve(
    resource="https://authoritative-source.com/topic",
    traverse_links=True,
    max_depth=2,
    max_pages=20,
    store_data=True,
    same_domain_only=False
)
```

## ⚙️ Configuration Options

### Depth Control
- **Depth 0**: Start page only
- **Depth 1**: Start page + directly linked pages
- **Depth 2**: Start page + linked pages + their links (default)
- **Depth 3+**: Deeper traversal (use carefully)

### Page Limits
- **Research**: 5-10 pages for focused topics
- **Documentation**: 15-25 pages for comprehensive coverage
- **Site Mapping**: 20-50 pages for structure overview

### Domain Restrictions
- **Same Domain Only**: Recommended for most use cases
- **External Links**: Use for research across multiple sources
- **Filtered Traversal**: Use include/exclude patterns for precision

## 🔧 Advanced Configuration

### Custom Link Patterns
The underlying traversal system supports custom include/exclude patterns:

```python
# Example: Focus on specific content types
traverse_website(
    start_url="https://site.com",
    include_patterns=[r"/articles/", r"/posts/", r"/guides/"],
    exclude_patterns=[r"/admin/", r"/login", r"\.pdf$"],
    max_depth=2,
    max_pages=15
)
```

### Performance Tuning
```python
# Respectful crawling
TraversalConfig(
    delay_between_requests=1.0,  # 1 second delay
    max_content_per_page=3000,   # Limit content length
    respect_robots_txt=True      # Honor robots.txt
)
```

## 🚦 Best Practices

### 1. **Start Small**
Begin with small page limits and shallow depths to understand the site structure:
```python
# Initial exploration
rival_retrieve(
    resource="https://new-site.com",
    traverse_links=True,
    max_depth=1,
    max_pages=3
)
```

### 2. **Use Appropriate Tools**
- **Research**: Use `research_website` for content discovery
- **Documentation**: Use `explore_docs` for technical sites
- **Structure**: Use `map_website` for site overviews
- **Custom**: Use `rival_retrieve` with traversal for specific needs

### 3. **Store Important Data**
Enable `store_data=True` for content you want to query later:
```python
research_website(
    url="https://important-research.com",
    max_pages=10,
    store_data=True
)

# Later, search the stored content
search_nodes(query="key research findings")
```

### 4. **Respect Rate Limits**
The system includes built-in delays and proxy rotation, but be mindful:
- Use reasonable page limits
- Don't traverse too aggressively
- Consider the target site's resources

### 5. **Monitor Results**
Check the traversal summary to understand what was discovered:
```python
result = research_website(url="https://site.com", max_pages=10)
print(f"Fetched {result.data.pages_fetched} pages")
print(f"Found {result.data.unique_links_found} unique links")
print(f"Max depth: {result.data.max_depth_reached}")
```

## 🌟 Key Features

| Feature | RivalSearchMCP |
|---------|----------------|
| **Link Following** | ✅ Intelligent depth control with customizable limits |
| **Content Extraction** | ✅ Full content extraction with OCR support |
| **Structured Output** | ✅ Type-safe Pydantic models for all responses |
| **Customization** | ✅ Extensive filtering and pattern matching options |
| **Data Storage** | ✅ Built-in graph storage with persistent memory |
| **Specialized Tools** | ✅ Research, documentation, and mapping tools |
| **Cost** | ✅ Completely free and self-hosted |
| **Privacy** | ✅ Fully local with no external data sharing |

## 🧪 Testing Link Traversal

### Test with MCP Inspector
```bash
# Start MCP Inspector
npx @modelcontextprotocol/inspector python src/server.py

# Test link traversal in the UI:
# Tool: research_website
# Parameters:
#   url: "https://example.com"
#   max_pages: 3
#   store_data: true
```

### Test Cases
1. **Documentation Site**: Test with docs.python.org
2. **Blog/Research**: Test with blog.openai.com
3. **Corporate Site**: Test with company homepages
4. **News Site**: Test with news article pages

## 🚨 Limitations & Considerations

### Technical Limitations
- **JavaScript Sites**: May miss dynamically loaded content
- **Authentication**: Cannot traverse login-protected content
- **Rate Limiting**: May be limited by target site restrictions
- **Large Sites**: Memory usage scales with page count

### Ethical Considerations
- **Respect robots.txt**: Built-in support for robots.txt compliance
- **Server Load**: Automatic delays prevent overwhelming target sites
- **Legal Compliance**: Ensure compliance with site terms of service
- **Data Privacy**: No data leaves your local system

## 📈 Performance Metrics

### Typical Performance
- **Page Fetch**: 2-5 seconds per page
- **Link Extraction**: ~100ms per page
- **Memory Usage**: ~50MB per 100 pages
- **Storage**: ~10KB per page in graph store

### Optimization Tips
- Use specific tools (research/docs/map) for better filtering
- Set appropriate page limits for your use case
- Enable data storage only when needed
- Monitor traversal summaries to optimize parameters

Link traversal makes RivalSearchMCP a powerful tool for comprehensive content discovery, research, and analysis. Combined with the existing search and reasoning capabilities, it provides a complete solution for AI-powered information gathering and knowledge building.