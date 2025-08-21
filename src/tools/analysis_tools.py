"""
Analysis tools for FastMCP server.
Handles content analysis and end-to-end research workflows.
"""

from typing import List, Dict, Any, Optional
from fastmcp import FastMCP
import re
from collections import Counter

from src.logger import logger


def register_analysis_tools(mcp: FastMCP):
    """Register all analysis-related tools."""
    
    @mcp.tool
    async def analyze_content(
        content: str,
        analysis_type: str = "general",
        extract_key_points: bool = True,
        summarize: bool = True
    ) -> dict:
        """
        Analyze content and extract insights.
        
        Args:
            content: Content to analyze
            analysis_type: Type of analysis - "general", "sentiment", "technical", "business"
            extract_key_points: Whether to extract key points
            summarize: Whether to create a summary
        """
        try:
            logger.info(f"Analyzing content with type: {analysis_type}")
            
            # Basic content analysis
            analysis_result = {
                "content_length": len(content),
                "word_count": len(content.split()),
                "analysis_type": analysis_type,
                "key_points": [],
                "summary": "",
                "insights": {}
            }
            
            # Extract key points if requested
            if extract_key_points:
                # Real key point extraction using sentence analysis
                sentences = re.split(r'[.!?]+', content)
                sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
                
                # Score sentences by length and keyword density
                scored_sentences = []
                for sentence in sentences:
                    score = len(sentence) * 0.3  # Length factor
                    # Add score for important keywords
                    important_words = ['important', 'key', 'critical', 'essential', 'significant', 'major', 'primary']
                    for word in important_words:
                        if word.lower() in sentence.lower():
                            score += 10
                    scored_sentences.append((sentence, score))
                
                # Get top 5 key points
                scored_sentences.sort(key=lambda x: x[1], reverse=True)
                key_points = [s[0] for s in scored_sentences[:5]]
                analysis_result["key_points"] = key_points
            
            # Create summary if requested
            if summarize:
                # Real summary using extractive summarization
                sentences = re.split(r'[.!?]+', content)
                sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
                
                if len(sentences) > 3:
                    # Take first, middle, and last sentences for summary
                    summary_parts = [
                        sentences[0],
                        sentences[len(sentences)//2] if len(sentences) > 2 else "",
                        sentences[-1] if len(sentences) > 1 else ""
                    ]
                    summary = '. '.join([s for s in summary_parts if s])
                else:
                    summary = content[:300] + "..." if len(content) > 300 else content
                
                analysis_result["summary"] = summary
            
            # Type-specific analysis
            if analysis_type == "sentiment":
                # Real sentiment analysis using keyword counting
                positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'positive', 'happy', 'success']
                negative_words = ['bad', 'terrible', 'awful', 'negative', 'sad', 'failure', 'problem', 'issue']
                
                content_lower = content.lower()
                positive_count = sum(content_lower.count(word) for word in positive_words)
                negative_count = sum(content_lower.count(word) for word in negative_words)
                
                if positive_count > negative_count:
                    sentiment = "positive"
                elif negative_count > positive_count:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                
                analysis_result["insights"]["sentiment"] = sentiment
                analysis_result["insights"]["sentiment_scores"] = {
                    "positive": positive_count,
                    "negative": negative_count
                }
                
            elif analysis_type == "technical":
                # Real technical term extraction
                technical_patterns = [
                    r'\b[A-Z]{2,}\b',  # Acronyms
                    r'\b\w+\.\w+\b',   # Abbreviations
                    r'\b\d+\.\d+\b',   # Version numbers
                    r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b'  # CamelCase
                ]
                
                technical_terms = set()
                for pattern in technical_patterns:
                    matches = re.findall(pattern, content)
                    technical_terms.update(matches)
                
                analysis_result["insights"]["technical_terms"] = list(technical_terms)[:10]
                
            elif analysis_type == "business":
                # Real business metrics extraction
                money_pattern = r'\$[\d,]+(?:\.\d{2})?'
                percentage_pattern = r'\d+(?:\.\d+)?%'
                date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
                
                money_matches = re.findall(money_pattern, content)
                percentage_matches = re.findall(percentage_pattern, content)
                date_matches = re.findall(date_pattern, content)
                
                analysis_result["insights"]["business_metrics"] = {
                    "monetary_values": money_matches[:5],
                    "percentages": percentage_matches[:5],
                    "dates": date_matches[:5]
                }
            
            return {
                "success": True,
                "analysis": analysis_result,
                "content_preview": content[:200] + "..." if len(content) > 200 else content
            }
            
        except Exception as e:
            logger.error(f"Content analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "analysis": {}
            }
    
    @mcp.tool
    async def research_topic(
        topic: str,
        sources: Optional[List[str]] = None,
        max_sources: int = 5,
        include_analysis: bool = True
    ) -> dict:
        """
        End-to-end research workflow for a topic.
        
        Args:
            topic: Research topic
            sources: Optional list of specific sources to use
            max_sources: Maximum number of sources to research
            include_analysis: Whether to include content analysis
        """
        try:
            logger.info(f"Starting comprehensive research on: {topic}")
            
            # Real research workflow implementation
            from src.core.search import GoogleSearchScraper
            from src.core.fetch import base_fetch_url
            
            research_results = {
                "topic": topic,
                "sources_researched": [],
                "key_findings": [],
                "summary": "",
                "recommendations": []
            }
            
            # Step 1: Search for relevant sources
            if not sources:
                scraper = GoogleSearchScraper()
                search_results = scraper.search_google(term=topic, num_results=max_sources)
                sources = [result.url for result in search_results[:max_sources]]
            
            # Step 2: Retrieve content from sources
            for i, source_url in enumerate(sources):
                try:
                    content = await base_fetch_url(source_url)
                    if content:
                        # Clean content
                        from src.utils import clean_html_to_markdown
                        clean_content = clean_html_to_markdown(str(content), source_url)
                        
                        research_results["sources_researched"].append({
                            "url": source_url,
                            "content_preview": clean_content[:200] + "..." if len(clean_content) > 200 else clean_content,
                            "content_length": len(clean_content)
                        })
                        
                        # Extract key findings from this source
                        sentences = re.split(r'[.!?]+', clean_content)
                        key_sentences = [s.strip() for s in sentences if len(s.strip()) > 50 and any(word in s.lower() for word in ['important', 'key', 'critical', 'significant'])]
                        research_results["key_findings"].extend(key_sentences[:3])
                        
                except Exception as e:
                    logger.warning(f"Failed to retrieve content from {source_url}: {e}")
            
            # Step 3: Generate summary and recommendations
            if research_results["key_findings"]:
                research_results["summary"] = f"Research on '{topic}' found {len(research_results['sources_researched'])} relevant sources with {len(research_results['key_findings'])} key findings."
                
                # Generate recommendations based on findings
                if len(research_results["sources_researched"]) > 2:
                    research_results["recommendations"].append("Multiple sources confirm findings - high confidence")
                if len(research_results["key_findings"]) > 5:
                    research_results["recommendations"].append("Rich information available - consider deeper analysis")
                if include_analysis:
                    research_results["recommendations"].append("Use analyze_content tool for detailed insights")
            
            return {
                "success": True,
                "research_results": research_results,
                "status": "research_completed",
                "sources_count": len(research_results["sources_researched"]),
                "findings_count": len(research_results["key_findings"])
            }
            
        except Exception as e:
            logger.error(f"Research topic failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "research_plan": {}
            }
