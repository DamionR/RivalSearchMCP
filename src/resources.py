"""
MCP Resources for RivalSearchMCP server.
Provides data access endpoints for LLMs to understand server capabilities and stored data.
"""

import json
from mcp.server import FastMCP
from src.data_store.manager import store_manager
from src.config import DEFAULT_UA_LIST, PAYWALL_INDICATORS, ARCHIVE_FALLBACKS


def register_resources(mcp: FastMCP):
    """Register all resources with the MCP server."""
    
    @mcp.resource("config://server-info")
    def get_server_info() -> str:
        """Get general information about RivalSearchMCP server capabilities."""
        info = {
            "name": "RivalSearchMCP",
            "version": "2.0.0",
            "description": "Advanced MCP server for web retrieval, data storage, and adaptive reasoning",
            "capabilities": {
                "web_retrieval": {
                    "bypass_protection": True,
                    "multi_format_support": ["HTML", "JSON", "images (OCR)", "streaming"],
                    "search_integration": "Google search with 'search:query' format",
                    "link_traversal": True,
                    "proxy_rotation": True
                },
                "data_storage": {
                    "type": "Graph-based (NetworkX)",
                    "operations": ["CRUD", "search", "relationships"],
                    "persistence": "JSON-based",
                    "query_interface": True
                },
                "reasoning": {
                    "type": "Adaptive step-by-step",
                    "features": ["branching", "revisions", "context_awareness"],
                    "multi_step": True
                },
                "transports": ["STDIO", "HTTP", "SSE"],
                "structured_outputs": True,
                "type_safety": "Pydantic models"
            },
            "tools_count": 15,
            "prompts_count": 8,
            "resources_count": 6
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
                    "parameters": ["url", "max_pages", "store_data"],
                    "use_cases": ["topic research", "content discovery"]
                },
                "explore_docs": {
                    "description": "Technical documentation site navigation",
                    "features": ["documentation patterns", "API focus"],
                    "parameters": ["url", "max_pages", "store_data"],
                    "use_cases": ["API documentation", "technical guides"]
                },
                "map_website": {
                    "description": "Website structure and content mapping",
                    "features": ["site architecture", "key page discovery"],
                    "parameters": ["url", "max_pages", "store_data"],
                    "use_cases": ["site audits", "competitive analysis"]
                },
                "stream_retrieve": {
                    "description": "Real-time WebSocket data streaming",
                    "features": ["live data feeds", "streaming content"],
                    "parameters": ["url"],
                    "use_cases": ["real-time data", "streaming APIs"]
                }
            },
            "ai_processing": {
                "adaptive_reason": {
                    "description": "Multi-step reasoning with branching support",
                    "features": ["revisions", "context awareness", "step-by-step analysis"],
                    "parameters": ["step_content", "step_num", "estimated_steps", "continue_reasoning"],
                    "use_cases": ["complex problem solving", "analysis", "reasoning chains"]
                }
            },
            "data_management": {
                "add_nodes": {
                    "description": "Store structured data as graph nodes",
                    "features": ["facts", "relationships", "persistent storage"],
                    "parameters": ["nodes"],
                    "use_cases": ["knowledge storage", "data persistence"]
                },
                "search_nodes": {
                    "description": "Query stored data by content",
                    "features": ["full-text search", "stored information"],
                    "parameters": ["query"],
                    "use_cases": ["information retrieval", "knowledge queries"]
                },
                "get_full_store": {
                    "description": "Retrieve complete knowledge graph",
                    "features": ["all nodes", "links", "relationships"],
                    "parameters": [],
                    "use_cases": ["data export", "full context"]
                }
            }
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
                    "research_website(url='promising_source', max_pages=8, store_data=True)",
                    "search_nodes(query='key findings')",
                    "adaptive_reason for analysis"
                ]
            },
            "documentation_exploration": {
                "description": "Explore technical documentation",
                "steps": [
                    "rival_retrieve(resource='https://docs.example.com')",
                    "explore_docs(url='https://docs.example.com', max_pages=20)",
                    "Store key information for reference"
                ]
            },
            "competitive_analysis": {
                "description": "Analyze competitor websites",
                "steps": [
                    "map_website(url='https://competitor.com', max_pages=25)",
                    "research_website(url='product_pages', max_pages=10)",
                    "Store and analyze findings"
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
    
    
    @mcp.resource("data://store-summary")
    def get_store_summary() -> str:
        """Get summary of currently stored data in the knowledge graph."""
        try:
            full_store = store_manager.get_full_store()
            
            summary = {
                "nodes_count": len(full_store.get('nodes', [])),
                "links_count": len(full_store.get('links', [])),
                "node_types": {},
                "recent_nodes": []
            }
            
            # Analyze node types
            nodes = full_store.get('nodes', [])
            for node in nodes:
                node_type = node.get('type', 'unknown')
                summary['node_types'][node_type] = summary['node_types'].get(node_type, 0) + 1
            
            # Get recent nodes (last 5)
            recent_nodes = nodes[-5:] if len(nodes) > 5 else nodes
            for node in recent_nodes:
                summary['recent_nodes'].append({
                    'name': node.get('name', 'unnamed'),
                    'type': node.get('type', 'unknown'),
                    'facts_count': len(node.get('facts', []))
                })
            
            if summary['nodes_count'] == 0:
                summary['message'] = "No data currently stored. Use store_data=True with retrieval tools to build knowledge base."
            
            return json.dumps(summary, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": f"Could not access data store: {str(e)}",
                "nodes_count": 0,
                "message": "Data store may be empty or inaccessible"
            }, indent=2)
    
    
    @mcp.resource("data://stored-nodes/{query}")
    def search_stored_nodes(query: str) -> str:
        """Search stored nodes by query and return matching results."""
        try:
            if not query or query.strip() == "":
                return json.dumps({
                    "error": "Query parameter is required",
                    "example": "Use: data://stored-nodes/your-search-term"
                }, indent=2)
            
            # Use the search functionality
            results = store_manager.search_nodes(query)
            
            search_results = {
                "query": query,
                "matches_found": len(results.get('nodes', [])),
                "nodes": [],
                "links": results.get('links', [])
            }
            
            # Format node results
            for node in results.get('nodes', []):
                search_results['nodes'].append({
                    'name': node.get('name', 'unnamed'),
                    'type': node.get('type', 'unknown'),
                    'facts': node.get('facts', [])[:5],  # Limit to first 5 facts
                    'total_facts': len(node.get('facts', []))
                })
            
            if search_results['matches_found'] == 0:
                search_results['message'] = f"No nodes found matching '{query}'. Try different search terms."
            
            return json.dumps(search_results, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": f"Search failed: {str(e)}",
                "query": query
            }, indent=2)
    
    
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