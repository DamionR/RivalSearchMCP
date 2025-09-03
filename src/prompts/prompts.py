"""
MCP Prompts for RivalSearchMCP server.
Provides reusable templates to guide LLM interactions with our tools.
"""

from fastmcp import FastMCP
from typing import Literal


def register_prompts(mcp: FastMCP):
    """Register all prompts with the MCP server."""
    
    @mcp.prompt
    def research_workflow_prompt(
        topic: str,
        depth: Literal["basic", "comprehensive", "expert"] = "comprehensive"
    ) -> str:
        """Generate a research workflow prompt for the given topic."""
        depth_instructions = {
            "basic": "Provide a high-level overview with key points",
            "comprehensive": "Include detailed analysis with multiple sources and insights",
            "expert": "Deep dive with technical details, expert insights, and actionable recommendations"
        }
        
        return f"""
        Research the topic: {topic}
        
        Please provide a {depth} analysis using the following systematic approach:
        
        1. INITIAL EXPLORATION (20% of effort):
           - Use google_search to understand the topic scope and current landscape
           - Identify key terminology and related concepts
           - Map out the main areas of interest
        
        2. TREND ANALYSIS (25% of effort):
           - Use search_trends to analyze current interest and patterns
           - Identify peak interest periods and seasonal variations
           - Compare related keywords and concepts
        
        3. CONTENT DISCOVERY (30% of effort):
           - Use traverse_website to explore authoritative sources
           - Extract and analyze key content using analyze_content
           - Map website structures and information hierarchies
        
        4. SYNTHESIS & INSIGHTS (25% of effort):
           - Combine findings from all sources
           - Identify patterns, trends, and key insights
           - Generate actionable recommendations
        
        DEPTH REQUIREMENTS: {depth_instructions[depth]}
        
        Use the available MCP tools systematically and provide structured findings.
        Focus on accuracy, comprehensiveness, and actionable insights.
        """

    @mcp.prompt
    def content_analysis_prompt(
        content_type: Literal["article", "website", "data", "trends"],
        analysis_focus: str
    ) -> str:
        """Generate a content analysis prompt."""
        return f"""
        Analyze this {content_type} content with focus on: {analysis_focus}
        
        ANALYSIS FRAMEWORK:
        
        1. CONTENT ASSESSMENT:
           - Identify main themes and key messages
           - Assess content quality and credibility
           - Extract key data points and insights
        
        2. PATTERN RECOGNITION:
           - Identify recurring themes and patterns
           - Note any trends or changes over time
           - Recognize relationships between different elements
        
        3. INSIGHT GENERATION:
           - Generate actionable insights
           - Identify opportunities and challenges
           - Provide strategic recommendations
        
        4. QUALITY EVALUATION:
           - Assess relevance and accuracy
           - Identify gaps or areas for improvement
           - Rate overall content value
        
        Please provide:
        - Key insights and main points
        - Patterns and trends identified
        - Relevance and credibility assessment
        - Actionable recommendations
        - Related topics for further exploration
        
        Use the available analysis tools to provide comprehensive insights.
        Focus on practical value and actionable intelligence.
        """

    @mcp.prompt
    def market_research_prompt(
        industry: str,
        research_scope: Literal["competitive", "trend", "opportunity", "comprehensive"] = "comprehensive"
    ) -> str:
        """Generate a market research prompt."""
        scope_instructions = {
            "competitive": "Focus on competitive landscape and market positioning",
            "trend": "Emphasize market trends and future directions",
            "opportunity": "Identify market opportunities and gaps",
            "comprehensive": "Cover all aspects of market research"
        }
        
        return f"""
        Conduct {research_scope} market research for the {industry} industry.
        
        RESEARCH OBJECTIVES:
        {scope_instructions[research_scope]}
        
        METHODOLOGY:
        
        1. MARKET LANDSCAPE ANALYSIS:
           - Use google_search to identify key players and market structure
           - Analyze industry terminology and key concepts
           - Map competitive landscape and market segments
        
        2. TREND ANALYSIS:
           - Use search_trends to analyze industry interest patterns
           - Identify emerging trends and declining areas
           - Compare related industry keywords and concepts
        
        3. COMPETITIVE INTELLIGENCE:
           - Use traverse_website to explore competitor websites
           - Analyze competitor positioning and messaging
           - Extract strategic insights and market approaches
        
        4. OPPORTUNITY IDENTIFICATION:
           - Identify market gaps and unmet needs
           - Analyze customer pain points and preferences
           - Generate strategic recommendations
        
        DELIVERABLES:
        - Market overview and key insights
        - Competitive analysis and positioning
        - Trend analysis and future outlook
        - Strategic recommendations and opportunities
        - Risk assessment and market challenges
        
        Use systematic research methods and provide evidence-based insights.
        Focus on actionable intelligence and strategic value.
        """

    @mcp.prompt
    def technical_research_prompt(
        technology: str,
        research_type: Literal["overview", "implementation", "comparison", "deep_dive"] = "overview"
    ) -> str:
        """Generate a technical research prompt."""
        type_instructions = {
            "overview": "Provide comprehensive technology overview and fundamentals",
            "implementation": "Focus on practical implementation and best practices",
            "comparison": "Compare multiple technologies and approaches",
            "deep_dive": "Deep technical analysis with advanced concepts"
        }
        
        return f"""
        Conduct {research_type} technical research on: {technology}
        
        RESEARCH FOCUS:
        {type_instructions[research_type]}
        
        TECHNICAL ANALYSIS FRAMEWORK:
        
        1. TECHNOLOGY FUNDAMENTALS:
           - Core concepts and principles
           - Architecture and design patterns
           - Key features and capabilities
        
        2. IMPLEMENTATION ANALYSIS:
           - Development approaches and methodologies
           - Best practices and common patterns
           - Tools and frameworks
        
        3. COMPARATIVE ANALYSIS:
           - Alternative technologies and approaches
           - Pros and cons of different solutions
           - Use case recommendations
        
        4. PRACTICAL APPLICATIONS:
           - Real-world use cases and examples
           - Implementation challenges and solutions
           - Performance and scalability considerations
        
        DELIVERABLES:
        - Technical overview and fundamentals
        - Implementation guidance and best practices
        - Comparative analysis and recommendations
        - Practical examples and use cases
        - Future trends and developments
        
        Use technical research tools and provide evidence-based technical insights.
        Focus on practical implementation and real-world applications.
        """

    # Keep existing prompts
    @mcp.prompt
    def retrieve_content_prompt(
        resource: str, limit: int = 5, extract_images: bool = False
    ) -> str:
        """Guide for enhanced content retrieval using retrieve_content."""
        image_instruction = (
            " and extract image text using OCR" if extract_images else ""
        )
        return f"""I need to retrieve content from: {resource}{image_instruction}
        
Please:
1. Use retrieve_content with resource="{resource}", limit={limit}, and extract_images={extract_images}
2. Extract the most relevant and comprehensive information
3. Focus on accuracy and completeness
4. Provide well-structured, clean content (no HTML)
5. Include proper attribution and context

Focus on comprehensive content retrieval and analysis."""

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

Focus on real-time data analysis and streaming content processing."""

    @mcp.prompt
    def google_search_prompt(
        query: str, num_results: int = 10, use_multi_engine: bool = False
    ) -> str:
        """Guide for comprehensive Google search using google_search."""
        engine_note = " with multi-engine fallback" if use_multi_engine else ""
        return f"""I need to search for: {query}{engine_note}
        
Please:
1. Use google_search with query="{query}", num_results={num_results}, and use_multi_engine={use_multi_engine}
2. Analyze search results for relevance and quality
3. Extract key information from top results
4. Focus on comprehensive search coverage
5. Provide structured search analysis

Focus on comprehensive search results and analysis."""

    @mcp.prompt
    def traverse_website_prompt(
        url: str, mode: str = "research", max_pages: int = 5
    ) -> str:
        """Guide for comprehensive website traversal using traverse_website."""
        return f"""I need to traverse the website: {url} in {mode} mode
        
Please:
1. Use traverse_website with url="{url}", mode="{mode}", and max_pages={max_pages}
2. Systematically explore the website structure
3. Extract key information from each page
4. Focus on:
   - Content organization and hierarchy
   - Key pages and sections
   - Important information and insights
   - Site structure patterns
5. Provide comprehensive website analysis

Focus on thorough website exploration and content discovery."""

    @mcp.prompt
    def analyze_content_prompt(content: str, analysis_type: str = "general") -> str:
        """Guide for content analysis using analyze_content."""
        return f"""I need to analyze content with type: {analysis_type}

Please:
1. Use analyze_content with content="{content[:200]}..." and analysis_type="{analysis_type}"
2. Extract key insights and patterns
3. Focus on:
   - Key points and main ideas
   - Content structure and organization
   - Important details and context
   - Actionable insights
4. Provide comprehensive content analysis
5. Generate actionable recommendations

Focus on deep content analysis and insight extraction."""

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

    @mcp.prompt
    def search_trends_prompt(
        keywords: list, timeframe: str = "today 12-m", geo: str = "US"
    ) -> str:
        """Guide for Google Trends analysis using search_trends."""
        keywords_str = ", ".join(keywords)
        return f"""I need to analyze trends for: {keywords_str}
        
Please:
1. Use search_trends with keywords={keywords}, timeframe="{timeframe}", and geo="{geo}"
2. Analyze trend patterns and insights
3. Focus on:
   - Interest trends over time
   - Peak interest periods
   - Comparative analysis between keywords
   - Geographic and temporal patterns
4. Provide comprehensive trend analysis
5. Generate actionable insights

Focus on trend analysis and pattern recognition."""

    @mcp.prompt
    def get_related_queries_prompt(
        keyword: str, timeframe: str = "today 12-m", geo: str = "US"
    ) -> str:
        """Guide for related queries analysis using get_related_queries."""
        return f"""I need to find related queries for: {keyword}
        
Please:
1. Use get_related_queries with keyword="{keyword}", timeframe="{timeframe}", and geo="{geo}"
2. Analyze related search patterns
3. Focus on:
   - Top related queries
   - Rising related queries
   - Search behavior insights
   - Content discovery opportunities
4. Provide comprehensive query analysis
5. Generate content and SEO insights

Focus on search behavior analysis and content discovery."""

    @mcp.prompt
    def get_interest_by_region_prompt(
        keyword: str, resolution: str = "COUNTRY", timeframe: str = "today 12-m"
    ) -> str:
        """Guide for regional interest analysis using get_interest_by_region."""
        return f"""I need to analyze regional interest for: {keyword}
        
Please:
1. Use get_interest_by_region with keyword="{keyword}", resolution="{resolution}", and timeframe="{timeframe}"
2. Analyze geographic interest patterns
3. Focus on:
   - High-interest regions
   - Geographic trends
   - Regional variations
   - Market opportunities
4. Provide comprehensive regional analysis
5. Generate geographic insights

Focus on geographic analysis and market insights."""

    @mcp.prompt
    def get_trending_searches_prompt(geo: str = "US") -> str:
        """Guide for trending searches analysis using get_trending_searches."""
        return f"""I need to find trending searches for: {geo}
        
Please:
1. Use get_trending_searches with geo="{geo}"
2. Analyze trending search patterns
3. Focus on:
   - Current trending topics
   - Search behavior insights
   - Content opportunities
   - Market trends
4. Provide comprehensive trending analysis
5. Generate content and marketing insights

Focus on trending analysis and opportunity identification."""

    @mcp.prompt
    def export_trends_prompt(
        keywords: list, timeframe: str = "today 12-m", geo: str = "US"
    ) -> str:
        """Guide for trends data export using export_trends_to_csv or export_trends_to_json."""
        keywords_str = ", ".join(keywords)
        return f"""I need to export trends data for: {keywords_str}
        
Please:
1. Use export_trends_to_csv or export_trends_to_json with keywords={keywords}, timeframe="{timeframe}", and geo="{geo}"
2. Choose appropriate export format (CSV for analysis, JSON for integration)
3. Focus on:
   - Data completeness and accuracy
   - Export file organization
   - Data analysis readiness
   - Integration capabilities
4. Provide export confirmation and file details
5. Generate data analysis recommendations

Focus on data export and analysis preparation."""

    @mcp.prompt
    def create_sql_table_prompt(
        keywords: list, timeframe: str = "today 12-m", geo: str = "US"
    ) -> str:
        """Guide for SQL table creation using create_sql_table."""
        keywords_str = ", ".join(keywords)
        return f"""I need to create a SQL table for trends data: {keywords_str}
        
Please:
1. Use create_sql_table with keywords={keywords}, timeframe="{timeframe}", and geo="{geo}"
2. Set up database structure for analysis
3. Focus on:
   - Table schema and columns
   - Data organization
   - Query optimization
   - Analysis capabilities
4. Provide database creation confirmation
5. Generate SQL query examples

Focus on database setup and data analysis preparation."""

    @mcp.prompt
    def compare_keywords_comprehensive_prompt(
        keywords: list, timeframe: str = "today 12-m", geo: str = "US"
    ) -> str:
        """Guide for comprehensive keyword comparison using compare_keywords_comprehensive."""
        keywords_str = ", ".join(keywords)
        return f"""I need to comprehensively compare keywords: {keywords_str}
        
Please:
1. Use compare_keywords_comprehensive with keywords={keywords}, timeframe="{timeframe}", and geo="{geo}"
2. Execute comprehensive analysis workflow
3. Focus on:
   - Trend comparison analysis
   - Related queries analysis
   - Regional interest comparison
   - Comprehensive insights
4. Provide structured comparison results
5. Generate actionable recommendations

Focus on comprehensive keyword analysis and comparison."""

    @mcp.prompt
    def generate_llms_txt_prompt(url: str) -> str:
        """Guide for LLMs.txt generation using generate_llms_txt."""
        return f"""I need to generate LLMs.txt files for: {url}
        
Please:
1. Use generate_llms_txt with url="{url}"
2. Execute comprehensive documentation generation
3. Focus on:
   - Website structure analysis
   - Content categorization
   - Documentation organization
   - LLMs.txt specification compliance
4. Provide generation confirmation and file details
5. Generate documentation insights

Focus on comprehensive documentation generation and organization."""
