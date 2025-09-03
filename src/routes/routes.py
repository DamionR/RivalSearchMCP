"""
Custom routes for RivalSearchMCP server.
Provides health checks, metrics, and monitoring endpoints.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from src.logging.logger import logger
from src.performance.performance import performance_monitor


def register_custom_routes(mcp):
    """Register custom routes with the FastMCP server."""
    
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> PlainTextResponse:
        """Health check endpoint for monitoring."""
        try:
            # Basic health check
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "server": "RivalSearchMCP",
                "version": "2.0.0"
            }
            
            # Check if we can access basic resources
            try:
                # This would check database connections, external services, etc.
                # For now, just return healthy
                pass
            except Exception as e:
                health_status["status"] = "degraded"
                health_status["warning"] = str(e)
            
            return PlainTextResponse(
                content="OK",
                status_code=HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return PlainTextResponse(
                content="ERROR",
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @mcp.custom_route("/metrics", methods=["GET"])
    async def metrics_endpoint(request: Request) -> JSONResponse:
        """Metrics endpoint for monitoring and observability."""
        try:
            # Get performance metrics
            performance_stats = performance_monitor.get_overall_stats()
            
            # Get system metrics
            system_metrics = {
                "timestamp": datetime.now().isoformat(),
                "server_name": "RivalSearchMCP",
                "version": "2.0.0",
                "environment": os.getenv("ENVIRONMENT", "development"),
                "uptime_seconds": performance_stats.get("uptime_seconds", 0),
                "total_operations": performance_stats.get("total_operations", 0),
                "total_errors": performance_stats.get("total_errors", 0),
                "overall_success_rate": performance_stats.get("overall_success_rate", 0),
                "overall_avg_time_ms": performance_stats.get("overall_avg_time_ms", 0)
            }
            
            # Get operation-specific metrics
            operation_metrics = {}
            for op_name in performance_stats.get("operations_tracked", []):
                op_stats = performance_monitor.get_operation_stats(op_name)
                if "error" not in op_stats:
                    operation_metrics[op_name] = op_stats
            
            metrics_data = {
                "system": system_metrics,
                "operations": operation_metrics,
                "summary": {
                    "total_operations_tracked": len(operation_metrics),
                    "healthy_operations": len([op for op in operation_metrics.values() if op.get("success_rate", 0) > 0.9]),
                    "degraded_operations": len([op for op in operation_metrics.values() if op.get("success_rate", 0) <= 0.9])
                }
            }
            
            return JSONResponse(
                content=metrics_data,
                status_code=HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Metrics endpoint failed: {e}")
            return JSONResponse(
                content={"error": str(e)},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @mcp.custom_route("/status", methods=["GET"])
    async def status_endpoint(request: Request) -> JSONResponse:
        """Detailed status endpoint for comprehensive server information."""
        try:
            status_data = {
                "server": {
                    "name": "RivalSearchMCP",
                    "version": "2.0.0",
                    "status": "operational",
                    "timestamp": datetime.now().isoformat()
                },
                "environment": {
                    "environment": os.getenv("ENVIRONMENT", "development"),
                    "port": os.getenv("PORT", "8000"),
                    "log_level": os.getenv("LOG_LEVEL", "INFO")
                },
                "capabilities": {
                    "search": True,
                    "trends": True,
                    "llms": True,
                    "traversal": True,
                    "analysis": True,
                    "retrieval": True
                },
                "performance": {
                    "uptime_seconds": performance_monitor.get_overall_stats().get("uptime_seconds", 0),
                    "total_operations": performance_monitor.get_overall_stats().get("total_operations", 0),
                    "success_rate": performance_monitor.get_overall_stats().get("overall_success_rate", 0)
                }
            }
            
            return JSONResponse(
                content=status_data,
                status_code=HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Status endpoint failed: {e}")
            return JSONResponse(
                content={"error": str(e)},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @mcp.custom_route("/info", methods=["GET"])
    async def info_endpoint(request: Request) -> JSONResponse:
        """Information endpoint for server details and configuration."""
        try:
            info_data = {
                "server_info": {
                    "name": "RivalSearchMCP",
                    "description": "Advanced Web Research and Content Discovery MCP Server",
                    "version": "2.0.0",
                    "author": "RivalSearchMCP Team",
                    "license": "MIT"
                },
                "features": {
                    "cloudflare_bypass": True,
                    "rich_snippets": True,
                    "traffic_estimation": True,
                    "ocr_support": True,
                    "multi_engine_fallback": True,
                    "comprehensive_research": True
                },
                "tools": {
                    "search": ["google_search", "multi_engine_search"],
                    "trends": ["search_trends", "compare_keywords", "export_trends"],
                    "llms": ["generate_llms_txt"],
                    "traversal": ["traverse_website", "extract_links"],
                    "analysis": ["analyze_content", "research_topic"],
                    "retrieval": ["retrieve_content", "stream_content"]
                },
                "endpoints": {
                    "health": "/health",
                    "metrics": "/metrics",
                    "status": "/status",
                    "info": "/info"
                }
            }
            
            return JSONResponse(
                content=info_data,
                status_code=HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Info endpoint failed: {e}")
            return JSONResponse(
                content={"error": str(e)},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @mcp.custom_route("/performance", methods=["GET"])
    async def performance_endpoint(request: Request) -> JSONResponse:
        """Performance analysis endpoint with recommendations."""
        try:
            from src.performance import create_performance_report
            
            performance_report = create_performance_report()
            
            return JSONResponse(
                content=performance_report,
                status_code=HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Performance endpoint failed: {e}")
            return JSONResponse(
                content={"error": str(e)},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @mcp.custom_route("/tools", methods=["GET"])
    async def tools_endpoint(request: Request) -> JSONResponse:
        """Tools information endpoint."""
        try:
            tools_info = {
                "search_tools": {
                    "google_search": {
                        "description": "Advanced Google Search with Cloudflare bypass",
                        "features": ["anti-detection", "rich_snippets", "traffic_estimation"],
                        "parameters": ["query", "num_results", "lang", "advanced"]
                    },
                    "multi_engine_search": {
                        "description": "Multi-engine search with fallbacks",
                        "features": ["fallback_support", "redundancy"],
                        "parameters": ["query", "engines", "num_results"]
                    }
                },
                "trends_tools": {
                    "search_trends": {
                        "description": "Google Trends analysis",
                        "features": ["temporal_analysis", "geographic_analysis"],
                        "parameters": ["keywords", "timeframe", "geo"]
                    },
                    "export_trends": {
                        "description": "Export trends data",
                        "features": ["csv_export", "json_export", "sql_export"],
                        "parameters": ["keywords", "format", "timeframe"]
                    }
                },
                "analysis_tools": {
                    "analyze_content": {
                        "description": "AI-powered content analysis",
                        "features": ["sentiment_analysis", "insight_extraction"],
                        "parameters": ["content", "analysis_type"]
                    },
                    "research_topic": {
                        "description": "End-to-end research workflow",
                        "features": ["workflow_orchestration", "multi_tool"],
                        "parameters": ["topic", "max_sources"]
                    }
                }
            }
            
            return JSONResponse(
                content=tools_info,
                status_code=HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Tools endpoint failed: {e}")
            return JSONResponse(
                content={"error": str(e)},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    logger.info("Custom routes registered successfully")
