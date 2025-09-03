"""
Resources module for RivalSearchMCP.
Provides data sources and dynamic content generators for MCP clients.
"""

from datetime import datetime
from typing import Dict, Any, List
from fastmcp import FastMCP


def register_resources(mcp: FastMCP):
    """Register all resources with the MCP server."""
    
    @mcp.resource("data://server/status")
    def get_server_status() -> dict:
        """Get current server status and capabilities."""
        return {
            "status": "operational",
            "version": "2.0.0",
            "name": "RivalSearchMCP",
            "tools_count": 15,
            "capabilities": [
                "search", "trends", "llms", "traversal", 
                "analysis", "retrieval", "content_processing"
            ],
            "features": {
                "cloudflare_bypass": True,
                "rich_snippets": True,
                "traffic_estimation": True,
                "ocr_support": True,
                "multi_engine_fallback": True
            },
            "timestamp": datetime.now().isoformat(),
            "uptime": "24h"  # This would be calculated in production
        }

    @mcp.resource("data://tools/categories")
    def get_tool_categories() -> dict:
        """Get organized tool categories for better discovery."""
        return {
            "search": {
                "description": "Web search and discovery tools",
                "tools": ["google_search", "multi_engine_search"],
                "features": ["anti-detection", "rich_snippets", "traffic_estimation"]
            },
            "trends": {
                "description": "Google Trends analysis and data export",
                "tools": [
                    "search_trends", "compare_keywords", "get_related_queries",
                    "get_interest_by_region", "export_trends", "create_sql_table"
                ],
                "features": ["data_export", "geographic_analysis", "temporal_analysis"]
            },
            "llms": {
                "description": "LLMs.txt generation and documentation",
                "tools": ["generate_llms_txt"],
                "features": ["website_analysis", "content_categorization", "llmstxt_spec"]
            },
            "traversal": {
                "description": "Website exploration and structure analysis",
                "tools": ["traverse_website", "extract_links"],
                "features": ["intelligent_crawling", "structure_mapping", "link_analysis"]
            },
            "analysis": {
                "description": "Content analysis and research workflows",
                "tools": ["analyze_content", "research_topic"],
                "features": ["ai_analysis", "insight_extraction", "workflow_orchestration"]
            },
            "retrieval": {
                "description": "Content retrieval and processing",
                "tools": ["retrieve_content", "stream_content"],
                "features": ["enhanced_retrieval", "ocr_support", "streaming"]
            }
        }

    @mcp.resource("data://tools/{tool_name}/schema")
    def get_tool_schema(tool_name: str) -> dict:
        """Get detailed schema for a specific tool."""
        tool_schemas = {
            "google_search": {
                "name": "google_search",
                "description": "Advanced Google Search with Cloudflare bypass",
                "parameters": {
                    "query": {"type": "string", "required": True, "description": "Search query"},
                    "num_results": {"type": "integer", "required": False, "default": 10, "range": [1, 100]},
                    "lang": {"type": "string", "required": False, "default": "en"},
                    "advanced": {"type": "boolean", "required": False, "default": True},
                    "use_multi_engine": {"type": "boolean", "required": False, "default": False}
                },
                "returns": {
                    "status": "string",
                    "method": "string", 
                    "results": "array",
                    "metadata": "object",
                    "query": "string",
                    "execution_time": "string"
                },
                "tags": ["search", "web", "primary", "google"],
                "features": ["anti_detection", "rich_snippets", "traffic_estimation"]
            },
            "search_trends": {
                "name": "search_trends",
                "description": "Google Trends analysis for keywords",
                "parameters": {
                    "keywords": {"type": "array", "required": True, "description": "Keywords to analyze"},
                    "timeframe": {"type": "string", "required": False, "default": "today 12-m"},
                    "geo": {"type": "string", "required": False, "default": "US"}
                },
                "returns": {
                    "status": "string",
                    "data": "object",
                    "metadata": "object"
                },
                "tags": ["trends", "analytics", "google"],
                "features": ["temporal_analysis", "geographic_analysis", "keyword_comparison"]
            },
            "analyze_content": {
                "name": "analyze_content",
                "description": "AI-powered content analysis and insights",
                "parameters": {
                    "content": {"type": "string", "required": True, "description": "Content to analyze"},
                    "analysis_type": {"type": "string", "required": False, "default": "general", "options": ["general", "sentiment", "technical", "business"]}
                },
                "returns": {
                    "analysis": "object",
                    "insights": "array",
                    "recommendations": "array"
                },
                "tags": ["analysis", "ai", "content"],
                "features": ["sentiment_analysis", "insight_extraction", "recommendation_generation"]
            }
        }
        
        if tool_name in tool_schemas:
            return tool_schemas[tool_name]
        else:
            return {
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(tool_schemas.keys())
            }

    @mcp.resource("data://performance/metrics")
    def get_performance_metrics() -> dict:
        """Get server performance metrics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "tools_called": 0,  # This would be tracked in production
                "requests_processed": 0,
                "average_response_time": 0.0,
                "success_rate": 1.0,
                "error_rate": 0.0
            },
            "status": "operational"
        }

    @mcp.resource("data://configuration/settings")
    def get_server_configuration() -> dict:
        """Get current server configuration."""
        return {
            "server_name": "RivalSearchMCP",
            "version": "2.0.0",
            "environment": "development",
            "features": {
                "include_fastmcp_meta": True,
                "on_duplicate_tools": "error",
                "on_duplicate_resources": "warn",
                "on_duplicate_prompts": "replace"
            },
            "capabilities": {
                "search": True,
                "trends": True,
                "llms": True,
                "traversal": True,
                "analysis": True,
                "retrieval": True
            }
        }

    @mcp.resource("data://help/usage_examples")
    def get_usage_examples() -> dict:
        """Get usage examples for common workflows."""
        return {
            "basic_search": {
                "description": "Simple web search",
                "tools": ["google_search"],
                "example": {
                    "tool": "google_search",
                    "parameters": {
                        "query": "Python web scraping",
                        "num_results": 10
                    }
                }
            },
            "trend_analysis": {
                "description": "Analyze keyword trends",
                "tools": ["search_trends", "compare_keywords"],
                "example": {
                    "tool": "search_trends",
                    "parameters": {
                        "keywords": ["Python", "JavaScript", "Go"],
                        "timeframe": "today 12-m",
                        "geo": "US"
                    }
                }
            },
            "website_analysis": {
                "description": "Analyze website structure and content",
                "tools": ["traverse_website", "analyze_content"],
                "example": {
                    "tool": "traverse_website",
                    "parameters": {
                        "url": "https://example.com",
                        "mode": "research",
                        "max_pages": 10
                    }
                }
            },
            "comprehensive_research": {
                "description": "End-to-end research workflow",
                "tools": ["research_topic"],
                "example": {
                    "tool": "research_topic",
                    "parameters": {
                        "topic": "Machine Learning in Healthcare",
                        "max_sources": 15
                    }
                }
            }
        }
