"""
MCP Resources for RivalSearchMCP server.
Provides data access endpoints for LLMs to understand server capabilities and configuration.
"""

import json
from fastmcp import FastMCP

from src.config import DEFAULT_UA_LIST, PAYWALL_INDICATORS, ARCHIVE_FALLBACKS


def register_resources(mcp: FastMCP):
    """Register all resources with the MCP server."""
    
    @mcp.resource("config://server-info")
    def get_server_info() -> str:
        """Get general information about RivalSearchMCP server capabilities."""
        info = {
            "name": "RivalSearchMCP",
            "version": "2.0.0",
            "description": "Advanced MCP server for web retrieval, search, and content discovery",
            "capabilities": {
                "web_retrieval": {
                    "bypass_protection": True,
                    "multi_format_support": ["HTML", "JSON", "images (OCR)", "streaming"],
                    "search_integration": "Google search with 'search:query' format",
                    "link_traversal": True,
                    "proxy_rotation": True
                },


                "transports": ["STDIO", "HTTP", "SSE"],
                "structured_outputs": True,
                "type_safety": "Pydantic models"
            },
            "tools_count": 8,
            "prompts_count": 8,
            "resources_count": 4
        }
        return json.dumps(info, indent=2)
    
    
    @mcp.resource("config://tools-overview")
    def get_tools_overview() -> str:
        """Get overview of all available tools organized by category."""
        tools = {
            "web_retrieval": {
                "rival_retrieve": {
                    "description": "Advanced web scraping with intelligent link traversal",
                    "features": ["bypass protection", "search integration", "multi-page discovery"],
                    "parameters": ["resource", "traverse_links", "max_depth", "max_pages"],
                    "use_cases": ["single page retrieval", "search queries", "link traversal"]
                },
                "research_website": {
                    "description": "Deep research across website content",
                    "features": ["content filtering", "research optimization"],
                    "parameters": ["url", "max_pages"],
                    "use_cases": ["topic research", "content discovery"]
                },
                "explore_docs": {
                    "description": "Technical documentation site navigation",
                    "features": ["documentation patterns", "API focus"],
                    "parameters": ["url", "max_pages"],
                    "use_cases": ["API documentation", "technical guides"]
                },
                "map_website": {
                    "description": "Website structure and content mapping",
                    "features": ["site architecture", "key page discovery"],
                    "parameters": ["url", "max_pages"],
                    "use_cases": ["site audits", "competitive analysis"]
                },
                "stream_retrieve": {
                    "description": "Real-time WebSocket data streaming",
                    "features": ["live data feeds", "streaming content"],
                    "parameters": ["url"],
                    "use_cases": ["real-time data", "streaming APIs"]
                }
            },


        }
        return json.dumps(tools, indent=2)
    
    
    @mcp.resource("config://usage-examples")
    def get_usage_examples() -> str:
        """Get practical usage examples for common scenarios."""
        examples = {
            "research_workflow": {
                "description": "Comprehensive research on a topic",
                "steps": [
                    "rival_retrieve(resource='search:topic', limit=10)",
                    "research_website(url='promising_source', max_pages=8)",
                    "Analyze and synthesize findings"
                ]
            },
            "documentation_exploration": {
                "description": "Explore technical documentation",
                "steps": [
                    "rival_retrieve(resource='https://docs.example.com')",
                    "explore_docs(url='https://docs.example.com', max_pages=20)",
                    "Extract and organize key information"
                ]
            },
            "competitive_analysis": {
                "description": "Analyze competitor websites",
                "steps": [
                    "map_website(url='https://competitor.com', max_pages=25)",
                    "research_website(url='product_pages', max_pages=10)",
                    "Analyze and document findings"
                ]
            },
            "link_traversal": {
                "description": "Deep content discovery",
                "steps": [
                    "rival_retrieve(resource='start_url', traverse_links=True, max_depth=2)",
                    "Configure traversal parameters based on needs",
                    "Use specialized tools for specific content types"
                ]
            }
        }
        return json.dumps(examples, indent=2)
    
    

    
    
    @mcp.resource("config://bypass-settings")
    def get_bypass_settings() -> str:
        """Get information about bypass and proxy settings."""
        settings = {
            "user_agents": {
                "count": len(DEFAULT_UA_LIST),
                "rotation": "Automatic rotation for each request",
                "examples": DEFAULT_UA_LIST[:3]  # Show first 3 examples
            },
            "paywall_detection": {
                "indicators_count": len(PAYWALL_INDICATORS),
                "detection": "Automatic paywall detection",
                "examples": PAYWALL_INDICATORS[:5]  # Show first 5 examples
            },
            "archive_fallbacks": {
                "services_count": len(ARCHIVE_FALLBACKS),
                "description": "Fallback to archive services when content is blocked",
                "services": ARCHIVE_FALLBACKS
            },
            "proxy_rotation": {
                "enabled": True,
                "description": "Automatic proxy detection and rotation",
                "sources": ["Free proxy lists", "Proxy rotation algorithms"]
            },
            "bypass_features": [
                "Anti-bot protection bypass",
                "Rate limit circumvention", 
                "Paywall detection and fallbacks",
                "User agent rotation",
                "Proxy rotation",
                "Archive service fallbacks"
            ]
        }
        return json.dumps(settings, indent=2)