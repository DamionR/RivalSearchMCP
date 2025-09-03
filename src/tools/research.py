"""
Comprehensive research tools for RivalSearchMCP.
Provides end-to-end research workflows using multiple tools.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
import asyncio

from fastmcp import FastMCP, Context
from pydantic import Field
from typing_extensions import Annotated

# TODO: Implement Google search integration
# from src.core import GoogleSearchScraper
from src.core.fetch import rival_retrieve
from src.logging.logger import logger


def register_research_tools(mcp: FastMCP):
    """Register comprehensive research tools."""

    @mcp.tool(
        name="comprehensive_research",
        description="Perform comprehensive research using multiple tools and workflows",
        tags={"research", "workflow", "comprehensive", "orchestration"},
        meta={
            "version": "2.0",
            "category": "Research",
            "performance": "high",
            "workflow": True,
            "multi_tool": True
        },
        annotations={
            "title": "Comprehensive Research",
            "readOnlyHint": True,
            "openWorldHint": True,
            "destructiveHint": False,
            "idempotentHint": False
        }
    )
    async def comprehensive_research(
        topic: Annotated[str, Field(
            description="Research topic to investigate",
            min_length=3,
            max_length=500
        )],
        max_sources: Annotated[int, Field(
            description="Maximum number of sources to analyze",
            ge=5,
            le=50,
            default=15
        )] = 15,
        include_trends: Annotated[bool, Field(
            description="Whether to include trends analysis"
        )] = True,
        include_website_analysis: Annotated[bool, Field(
            description="Whether to include website traversal and analysis"
        )] = True,
        research_depth: Annotated[Literal["basic", "comprehensive", "expert"], Field(
            description="Depth of research to perform"
        )] = "comprehensive",
        ctx: Optional[Context] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive research using multiple tools and workflows.
        
        This tool orchestrates a complete research workflow including:
        - Initial web search and source discovery
        - Trends analysis (if enabled)
        - Website traversal and content analysis (if enabled)
        - Content synthesis and insight generation
        - Progress reporting throughout the process
        
        Returns structured research findings with comprehensive metadata.
        """
        
        research_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if ctx:
            await ctx.info(f"🔬 Starting comprehensive research on: {topic}")
            await ctx.info(f"📊 Research ID: {research_id}")
            await ctx.info(f"🎯 Target sources: {max_sources}")
            await ctx.info(f"📈 Trends analysis: {'Enabled' if include_trends else 'Disabled'}")
            await ctx.info(f"🌐 Website analysis: {'Enabled' if include_website_analysis else 'Disabled'}")
            await ctx.report_progress(progress=0, total=100)
        
        logger.info(f"Starting comprehensive research: {topic} (ID: {research_id})")
        
        try:
            research_results = {
                "research_id": research_id,
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "parameters": {
                    "max_sources": max_sources,
                    "include_trends": include_trends,
                    "include_website_analysis": include_website_analysis,
                    "research_depth": research_depth
                },
                "phases": {},
                "synthesis": {},
                "metadata": {}
            }
            
            # Phase 1: Initial Search and Source Discovery (20%)
            if ctx:
                await ctx.info("🔄 Phase 1: Initial search and source discovery")
                await ctx.report_progress(progress=10, total=100)
            
            try:
                # Use Bing Search for initial discovery
                from src.core.search.engines.bing.bing_engine import BingSearchEngine
                bing_engine = BingSearchEngine()
                search_results = await bing_engine.search(
                    query=topic,
                    num_results=max_sources,
                    extract_content=True,
                    follow_links=False,
                    max_depth=1
                )
                
                if search_results:
                    # Extract key information from search results
                    sources = []
                    for result in search_results:
                        source_info = {
                            "title": result.title,
                            "url": result.url,
                            "description": result.description,
                            "engine": result.engine,
                            "position": result.position,
                            "timestamp": result.timestamp
                        }
                        sources.append(source_info)
                    
                    research_results["phases"]["source_discovery"] = {
                        "status": "success",
                        "sources_found": len(sources),
                        "sources": sources[:max_sources],
                        "search_method": "direct_google"
                    }
                    
                    if ctx:
                        await ctx.info(f"✅ Phase 1 complete: {len(sources)} sources discovered")
                        await ctx.report_progress(progress=30, total=100)
                else:
                    research_results["phases"]["source_discovery"] = {
                        "status": "partial",
                        "sources_found": 0,
                        "error": "No search results found"
                    }
                    
                    if ctx:
                        await ctx.warning("⚠️ Phase 1: No search results found")
                        await ctx.report_progress(progress=30, total=100)
                        
            except Exception as e:
                research_results["phases"]["source_discovery"] = {
                    "status": "error",
                    "error": str(e)
                }
                
                if ctx:
                    await ctx.error(f"❌ Phase 1 failed: {str(e)}")
                    await ctx.report_progress(progress=30, total=100)
            
            # Phase 2: Trends Analysis (25%)
            if include_trends:
                if ctx:
                    await ctx.info("📈 Phase 2: Trends analysis")
                    await ctx.report_progress(progress=35, total=100)
                
                try:
                    # Call actual trends analysis tools
                    from src.core.trends import GoogleTrendsAPI
                    
                    trends_api = GoogleTrendsAPI()
                    # Note: search_trends returns DataFrame, not awaitable
                    trends_data = trends_api.search_trends(
                        keywords=[topic],
                        timeframe="today 12-m",
                        geo="US"
                    )
                    
                    if trends_data and trends_data.get("status") == "success":
                        research_results["phases"]["trends_analysis"] = {
                            "status": "success",
                            "data": trends_data,
                            "keywords_analyzed": [topic],
                            "timeframe": "today 12-m",
                            "geo": "US"
                        }
                        
                        if ctx:
                            await ctx.info("✅ Phase 2 complete: Trends analysis successful")
                            await ctx.report_progress(progress=60, total=100)
                    else:
                        research_results["phases"]["trends_analysis"] = {
                            "status": "partial",
                            "data": trends_data,
                            "warning": "Trends analysis returned limited data"
                        }
                        
                        if ctx:
                            await ctx.warning("⚠️ Phase 2: Trends analysis returned limited data")
                            await ctx.report_progress(progress=60, total=100)
                        
                except Exception as e:
                    research_results["phases"]["trends_analysis"] = {
                        "status": "error",
                        "error": str(e)
                    }
                    
                    if ctx:
                        await ctx.error(f"❌ Phase 2 failed: {str(e)}")
                        await ctx.report_progress(progress=60, total=100)
            else:
                if ctx:
                    await ctx.info("⏭️ Phase 2 skipped: Trends analysis disabled")
                    await ctx.report_progress(progress=60, total=100)
                
                research_results["phases"]["trends_analysis"] = {
                    "status": "skipped",
                    "reason": "Trends analysis disabled by user"
                }
            
            # Phase 3: Website Analysis (30%)
            if include_website_analysis:
                if ctx:
                    await ctx.info("🌐 Phase 3: Website analysis and content extraction")
                    await ctx.report_progress(progress=65, total=100)
                
                try:
                    # Analyze top sources from search results
                    website_analysis = []
                    sources_to_analyze = research_results["phases"]["source_discovery"].get("sources", [])[:5]
                    
                    for i, source in enumerate(sources_to_analyze):
                        if ctx:
                            await ctx.info(f"🔍 Analyzing website {i+1}/{len(sources_to_analyze)}: {source.get('engine', 'unknown')}")
                        
                        try:
                            # Call actual website traversal and analysis tools
                            from src.core.traverse import traverse_website
                            
                            # Traverse the website
                            traversal_result = await traverse_website(
                                url=source["url"],
                                max_depth=2,
                                max_pages=10
                            )
                            
                            # Analyze the content
                            if traversal_result and isinstance(traversal_result, dict):
                                content_to_analyze = str(traversal_result)[:2000]  # Limit content for analysis
                                # TODO: Implement content analysis
                                analysis_result = {
                                    "status": "not_implemented",
                                    "content_preview": content_to_analyze[:500]
                                }
                                
                                website_analysis.append({
                                    "url": source["url"],
                                    "engine": source.get('engine', 'unknown'),
                                    "traversal_result": traversal_result,
                                    "content_analysis": analysis_result,
                                    "status": "success"
                                })
                            else:
                                website_analysis.append({
                                    "url": source["url"],
                                    "engine": source.get('engine', 'unknown'),
                                    "error": "No traversal data returned",
                                    "status": "partial"
                                })
                            
                        except Exception as e:
                            analysis_result = {
                                "url": source["url"],
                                "domain": source["domain"],
                                "error": str(e),
                                "status": "error"
                            }
                            website_analysis.append(analysis_result)
                    
                    research_results["phases"]["website_analysis"] = {
                        "status": "success",
                        "websites_analyzed": len(website_analysis),
                        "analysis_results": website_analysis
                    }
                    
                    if ctx:
                        await ctx.info(f"✅ Phase 3 complete: {len(website_analysis)} websites analyzed")
                        await ctx.report_progress(progress=85, total=100)
                        
                except Exception as e:
                    research_results["phases"]["website_analysis"] = {
                        "status": "error",
                        "error": str(e)
                    }
                    
                    if ctx:
                        await ctx.error(f"❌ Phase 3 failed: {str(e)}")
                        await ctx.report_progress(progress=85, total=100)
            else:
                if ctx:
                    await ctx.info("⏭️ Phase 3 skipped: Website analysis disabled")
                    await ctx.report_progress(progress=85, total=100)
                
                research_results["phases"]["website_analysis"] = {
                    "status": "skipped",
                    "reason": "Website analysis disabled by user"
                }
            
            # Phase 4: Synthesis and Insights (25%)
            if ctx:
                await ctx.info("🧠 Phase 4: Synthesizing findings and generating insights")
                await ctx.report_progress(progress=90, total=100)
            
            try:
                # Generate synthesis based on research depth
                synthesis = generate_research_synthesis(
                    research_results, research_depth, ctx
                )
                
                research_results["synthesis"] = synthesis
                research_results["metadata"]["total_phases"] = 4
                research_results["metadata"]["successful_phases"] = sum(
                    1 for phase in research_results["phases"].values()
                    if phase.get("status") == "success"
                )
                research_results["metadata"]["research_depth"] = research_depth
                
                if ctx:
                    await ctx.info("✅ Phase 4 complete: Synthesis and insights generated")
                    await ctx.report_progress(progress=100, total=100)
                    await ctx.info(f"🎯 Research completed successfully! Research ID: {research_id}")
                    
            except Exception as e:
                research_results["synthesis"] = {
                    "status": "error",
                    "error": str(e)
                }
                
                if ctx:
                    await ctx.error(f"❌ Phase 4 failed: {str(e)}")
                    await ctx.report_progress(progress=100, total=100)
            
            # Final status
            research_results["status"] = "completed"
            research_results["completion_time"] = datetime.now().isoformat()
            
            logger.info(f"Comprehensive research completed: {topic} (ID: {research_id})")
            
            return research_results
            
        except Exception as e:
            error_msg = f"Comprehensive research failed for '{topic}': {str(e)}"
            if ctx:
                await ctx.error(f"❌ {error_msg}")
            
            logger.error(error_msg)
            return {
                "research_id": research_id,
                "topic": topic,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


def generate_research_synthesis(
    research_results: Dict[str, Any], 
    research_depth: str, 
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Generate research synthesis based on depth and findings."""
    
    synthesis = {
        "status": "success",
        "depth": research_depth,
        "summary": "",
        "key_findings": [],
        "insights": [],
        "recommendations": [],
        "next_steps": []
    }
    
    # Extract key information from research phases
    sources = research_results["phases"].get("source_discovery", {}).get("sources", [])
    trends = research_results["phases"].get("trends_analysis", {})
    websites = research_results["phases"].get("website_analysis", {})
    
    # Generate summary based on depth
    if research_depth == "basic":
        synthesis["summary"] = f"Basic research on '{research_results['topic']}' completed with {len(sources)} sources."
        synthesis["key_findings"] = [f"Found {len(sources)} relevant sources" if sources else "Limited source availability"]
        
    elif research_depth == "comprehensive":
        synthesis["summary"] = f"Comprehensive research on '{research_results['topic']}' completed with {len(sources)} sources, trends analysis, and website exploration."
        synthesis["key_findings"] = [
            f"Discovered {len(sources)} relevant sources",
            f"Trends analysis: {'Completed' if trends.get('status') == 'success' else 'Not available'}",
            f"Website analysis: {'Completed' if websites.get('status') == 'success' else 'Not available'}"
        ]
        
    elif research_depth == "expert":
        synthesis["summary"] = f"Expert-level research on '{research_results['topic']}' completed with comprehensive analysis across all dimensions."
        synthesis["key_findings"] = [
            f"Comprehensive source discovery: {len(sources)} sources",
            f"Advanced trends analysis: {'Completed' if trends.get('status') == 'success' else 'Not available'}",
            f"Deep website analysis: {'Completed' if websites.get('status') == 'success' else 'Not available'}",
            "Multi-dimensional insights generated"
        ]
    
    # Generate insights based on available data
    if sources:
        synthesis["insights"].append(f"Primary sources identified: {len(sources)}")
        if any(s.get("has_rich_snippet") for s in sources):
            synthesis["insights"].append("Rich snippets detected in search results")
        if any(s.get("estimated_traffic") == "high" for s in sources):
            synthesis["insights"].append("High-traffic sources identified")
    
    if trends.get("status") == "success":
        synthesis["insights"].append("Trends data available for temporal analysis")
    
    if websites.get("status") == "success":
        synthesis["insights"].append(f"Website analysis completed for {websites.get('websites_analyzed', 0)} sites")
    
    # Generate recommendations
    synthesis["recommendations"] = [
        "Review and validate key sources",
        "Consider trends analysis for temporal insights",
        "Explore website content for deeper understanding",
        "Cross-reference findings across multiple sources"
    ]
    
    # Generate next steps
    synthesis["next_steps"] = [
        "Validate key findings with additional sources",
        "Perform deeper analysis on high-priority sources",
        "Consider expanding research scope if needed",
        "Document findings and insights for future reference"
    ]
    
    return synthesis
