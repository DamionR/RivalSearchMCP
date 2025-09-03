#!/usr/bin/env python3
"""
RivalSearchMCP Server - Advanced Web Research and Content Discovery
"""

import os
from fastmcp import FastMCP

# Import modular tool registration functions
from src.tools.retrieval import register_retrieval_tools
from src.tools.search import register_search_tools
from src.tools.traversal import register_traversal_tools
from src.tools.analysis import register_analysis_tools
from src.tools.trends import register_trends_tools
from src.tools.llms import register_llms_tools
from src.tools.research import register_research_tools

# Import prompts
from src.prompts import register_prompts

# Import resources
from src.resources import register_resources

# Import middleware
from src.middleware import register_middleware

# Import custom routes
from src.routes.routes import register_custom_routes

# Import logger
from src.logging.logger import logger

# Environment-based configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Comprehensive server instructions
SERVER_INSTRUCTIONS = """
Advanced web research and content discovery MCP server.

CAPABILITIES:
- Google Search scraping with Cloudflare bypass and anti-detection
- Google Trends analysis with data export (CSV, JSON, SQL)
- LLMs.txt generation for websites following llmstxt.org specification
- Website traversal and structure analysis with intelligent crawling
- Content extraction and processing with OCR support
- Multi-engine search with automatic fallbacks
- Comprehensive research workflows combining multiple tools

AVAILABLE TOOLS:
Search & Discovery:
- google_search: Advanced Google search with rich snippets detection
- multi_engine_search: Fallback search using multiple engines
- retrieve_content: Enhanced content retrieval from URLs
- stream_content: Real-time streaming content processing

Trends & Analytics:
- search_trends: Google Trends analysis for keywords
- compare_keywords: Comprehensive keyword comparison
- get_related_queries: Find related search terms
- get_interest_by_region: Geographic interest analysis
- export_trends: Export trends data in multiple formats
- create_sql_table: Database setup for trends analysis

Content Analysis:
- analyze_content: AI-powered content analysis and insights
- research_topic: End-to-end research workflow
- traverse_website: Intelligent website exploration
- extract_links: Link extraction and analysis

Research & Workflows:
- comprehensive_research: Multi-phase research with progress tracking
- research_workflow_prompt: Structured research guidance
- market_research_prompt: Industry analysis templates
- technical_research_prompt: Technology research frameworks

Documentation:
- generate_llms_txt: Generate LLMs.txt files for websites

USAGE PATTERNS:
1. Basic Research: Use google_search for simple queries
2. Trend Analysis: Use search_trends + export_trends for market research
3. Content Discovery: Use traverse_website + analyze_content for deep analysis
4. Comprehensive Research: Use comprehensive_research for end-to-end workflows
5. Documentation: Use generate_llms_txt for website documentation

BEST PRACTICES:
- Provide specific, detailed search queries for better results
- Use appropriate result limits (10-50 for search, 100+ for trends)
- Combine multiple tools for comprehensive research workflows
- Use trends tools for market research and content strategy
- Leverage traversal tools for website analysis and mapping

PERFORMANCE NOTES:
- Search tools include automatic rate limiting and anti-detection
- Trends analysis supports multiple timeframes and geographic regions
- Content analysis includes OCR for image text extraction
- All tools provide progress reporting and detailed logging
- Comprehensive research tools include multi-phase progress tracking

MONITORING & HEALTH:
- Health check endpoint: /health
- Performance metrics: /metrics
- Server status: /status
- Tools information: /tools
- Performance analysis: /performance
"""

# Create enhanced FastMCP server instance
app = FastMCP(
    name="RivalSearchMCP",
    instructions=SERVER_INSTRUCTIONS,
    include_fastmcp_meta=True,  # Enable rich metadata
    on_duplicate_tools="error",  # Prevent conflicts
    on_duplicate_resources="warn",
    on_duplicate_prompts="replace"
)

# Register middleware for production readiness
register_middleware(app)

# Register all tools using modular approach
register_retrieval_tools(app)
register_search_tools(app)
register_traversal_tools(app)
register_analysis_tools(app)
register_trends_tools(app)
register_llms_tools(app)
register_research_tools(app)

# Register prompts
register_prompts(app)

# Register resources
register_resources(app)

# Register custom routes
register_custom_routes(app)

if __name__ == "__main__":
    if ENVIRONMENT == "production":
        logger.info(f"Starting RivalSearchMCP in production mode on port {PORT}")
        app.run(
            transport="http",
            host="0.0.0.0",
            port=PORT,
            log_level=LOG_LEVEL
        )
    else:
        logger.info("Starting RivalSearchMCP in development mode (stdio)")
        # For CLI compatibility, run directly with STDIO transport
        app.run()