# RivalSearchMCP Usage Guide

## Overview

RivalSearchMCP provides 6 powerful tools for web research and content discovery. This guide shows you how to use each tool effectively.

## Available Tools

### 1. `retrieve_content` - Enhanced Content Retrieval

Get content from URLs, search queries, or multiple resources with image extraction support.

**Parameters:**
- `resource`: Single URL, list of URLs, or search query (e.g., "search:python")
- `limit`: Maximum number of results for batch operations (default: 5)
- `max_length`: Maximum content length per result (default: 2000)
- `extract_images`: Whether to extract and process images with OCR (default: False)

**Examples:**
```python
# Get content from a single URL
retrieve_content(resource="https://example.com")

# Search Google
retrieve_content(resource="search:artificial intelligence trends 2024", limit=10)

# Get content from multiple URLs
retrieve_content(resource=["https://site1.com", "https://site2.com"], limit=3)

# Extract text from images
retrieve_content(resource="https://example.com", extract_images=True)
```

### 2. `stream_content` - WebSocket Streaming

Retrieve real-time streaming content from WebSocket URLs.

**Parameters:**
- `url`: WebSocket URL to connect to

**Example:**
```python
# Get streaming content
stream_content(url="wss://echo.websocket.org")
```

### 3. `google_search` - Comprehensive Google Search

Advanced Google Search with multi-engine fallback and rich metadata.

**Parameters:**
- `query`: Search query
- `num_results`: Number of results to return (default: 10)
- `lang`: Language for search (default: "en")
- `advanced`: Enable advanced features like rich snippets detection (default: True)
- `use_multi_engine`: Use multi-engine search as fallback (default: False)
- `safe`: Safe search setting ("active", "off") (default: "active")
- `region`: Geographic region for search
- `timeout`: Request timeout in seconds (default: 5)

**Example:**
```python
# Basic search
google_search(query="Python programming", num_results=15)

# Advanced search with fallback
google_search(
    query="machine learning tutorials",
    num_results=20,
    advanced=True,
    use_multi_engine=True,
    region="US"
)
```

### 4. `traverse_website` - Website Exploration

Comprehensive website traversal with different modes for different use cases.

**Parameters:**
- `url`: Website URL to traverse
- `mode`: Traversal mode - "research" (general), "docs" (documentation), "map" (structure) (default: "research")
- `max_pages`: Maximum number of pages to traverse (default: 5)
- `max_depth`: Maximum depth for mapping mode (default: 2)

**Examples:**
```python
# General research mode
traverse_website(url="https://blog.example.com", mode="research", max_pages=10)

# Documentation exploration
traverse_website(url="https://docs.example.com", mode="docs", max_pages=20)

# Website structure mapping
traverse_website(url="https://competitor.com", mode="map", max_pages=15, max_depth=3)
```

### 5. `analyze_content` - Content Analysis

Analyze content and extract insights with different analysis types.

**Parameters:**
- `content`: Content to analyze
- `analysis_type`: Type of analysis - "general", "sentiment", "technical", "business" (default: "general")
- `extract_key_points`: Whether to extract key points (default: True)
- `summarize`: Whether to create a summary (default: True)

**Examples:**
```python
# General analysis
analyze_content(content="Your content here...", analysis_type="general")

# Sentiment analysis
analyze_content(content="Product review text...", analysis_type="sentiment")

# Technical analysis
analyze_content(content="Technical documentation...", analysis_type="technical")

# Business analysis
analyze_content(content="Business report...", analysis_type="business")
```

### 6. `research_topic` - End-to-End Research

Complete research workflow that searches, retrieves, and analyzes content for a topic.

**Parameters:**
- `topic`: Research topic
- `sources`: Optional list of specific sources to use
- `max_sources`: Maximum number of sources to research (default: 5)
- `include_analysis`: Whether to include content analysis (default: True)

**Example:**
```python
# Research a topic
research_topic(topic="climate change solutions", max_sources=8)

# Research with specific sources
research_topic(
    topic="AI ethics",
    sources=["https://ai.org/ethics", "https://research.ai/guidelines"],
    include_analysis=True
)
```

## Common Workflows

### Basic Web Research
```python
# 1. Search for information
results = google_search(query="your topic", num_results=10)

# 2. Get content from top results
content = retrieve_content(resource="https://top-result.com")

# 3. Analyze the content
analysis = analyze_content(content=content, analysis_type="general")
```

### Comprehensive Topic Research
```python
# Use the research workflow
research = research_topic(topic="your research topic", max_sources=10)
```

### Website Analysis
```python
# Explore a website thoroughly
pages = traverse_website(url="https://target-site.com", mode="research", max_pages=15)

# Analyze key pages
for page in pages[:3]:
    analysis = analyze_content(content=page['content'], analysis_type="business")
```

## Tips for Best Results

1. **Use appropriate tools for your needs:**
   - `retrieve_content` for single pages or searches
   - `google_search` for comprehensive search results
   - `traverse_website` for exploring entire sites
   - `analyze_content` for extracting insights
   - `research_topic` for complete research workflows

2. **Optimize parameters:**
   - Start with smaller `max_pages` values and increase as needed
   - Use `extract_images=True` when content includes important images
   - Enable `use_multi_engine=True` for more reliable search results

3. **Combine tools effectively:**
   - Use `google_search` to find sources, then `retrieve_content` for details
   - Use `traverse_website` to explore sites, then `analyze_content` for insights
   - Use `research_topic` for comprehensive research projects