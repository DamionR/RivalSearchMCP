"""
MCP Prompts for RivalSearchMCP server.
Provides reusable templates to guide LLM interactions with our tools.
"""

from fastmcp import FastMCP


def register_prompts(mcp: FastMCP):
    """Register all prompts with the MCP server."""
    
    @mcp.prompt
    def retrieve_content_prompt(resource: str, limit: int = 5, extract_images: bool = False) -> str:
        """Guide for enhanced content retrieval using retrieve_content."""
        image_instruction = " and extract image text using OCR" if extract_images else ""
        return f"""I need to retrieve content from: {resource}{image_instruction}

Please:
1. Use retrieve_content with resource="{resource}", limit={limit}, and extract_images={extract_images}
2. Extract the most relevant and comprehensive information
3. Focus on accuracy and completeness
4. Provide well-structured, clean content (no HTML)
5. Include proper attribution and context

Deliver high-quality, formatted content suitable for analysis."""


    @mcp.prompt
    def stream_content_prompt(url: str) -> str:
        """Guide for retrieving streaming content using stream_content."""
        return f"""I need to retrieve streaming content from: {url}

Please:
1. Use stream_content to get real-time streaming content
2. Monitor the stream for relevant information
3. Extract key data points and insights
4. Provide analysis of the streaming content (no HTML)
5. Note any patterns or trends in the data

Focus on real-time data extraction and analysis."""


    @mcp.prompt
    def traverse_website_prompt(url: str, mode: str = "research", max_pages: int = 5) -> str:
        """Guide for comprehensive website traversal using traverse_website."""
        return f"""I need to traverse the website: {url} in {mode} mode

Please:
1. Use traverse_website with url="{url}", mode="{mode}", and max_pages={max_pages}
2. Explore the website systematically based on the mode:
   - research: General content exploration
   - docs: Documentation-specific navigation
   - map: Website structure mapping
3. Extract key information from multiple pages
4. Provide structured analysis of the website content
5. Focus on comprehensive coverage and insights

Deliver thorough website analysis with clean, formatted content."""


    @mcp.prompt
    def google_search_prompt(query: str, num_results: int = 10) -> str:
        """Guide for comprehensive Google search using the combined google_search tool."""
        return f"""I need comprehensive search results for: "{query}"

Please:
1. Use google_search with query="{query}" and num_results={num_results}
2. Analyze the search results for relevance and quality
3. Extract key information from the top results
4. Identify patterns in search results and metadata
5. Provide insights on:
   - Search result quality and relevance
   - Featured content and snippets
   - Source credibility and diversity
   - Search metadata and features

Focus on comprehensive search analysis and result evaluation."""


    @mcp.prompt
    def analyze_content_prompt(content: str, analysis_type: str = "general") -> str:
        """Guide for content analysis using analyze_content."""
        return f"""I need to analyze content with type: {analysis_type}

Please:
1. Use analyze_content with content and analysis_type="{analysis_type}"
2. Extract key insights and patterns from the content
3. Provide structured analysis based on the type:
   - general: Overall content analysis
   - sentiment: Sentiment analysis
   - technical: Technical term extraction
   - business: Business metrics analysis
4. Generate actionable insights and recommendations
5. Focus on extracting meaningful, structured information

Deliver comprehensive content analysis with actionable insights."""


    @mcp.prompt
    def research_topic_prompt(topic: str, max_sources: int = 5) -> str:
        """Guide for end-to-end research using research_topic."""
        return f"""I need to conduct comprehensive research on: {topic}

Please:
1. Use research_topic with topic="{topic}" and max_sources={max_sources}
2. Execute a complete research workflow:
   - Search for relevant sources
   - Retrieve and analyze content
   - Synthesize findings
   - Generate insights
3. Provide structured research results
4. Include key findings and recommendations
5. Focus on comprehensive, actionable research

Deliver end-to-end research with actionable insights and recommendations."""


