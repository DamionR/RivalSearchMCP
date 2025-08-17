"""
MCP Prompts for RivalSearchMCP server.
Provides reusable templates to guide LLM interactions with our tools.
"""

from mcp.server import FastMCP


def register_prompts(mcp: FastMCP):
    """Register all prompts with the MCP server."""
    
    @mcp.prompt("web-research")
    def web_research_prompt(topic: str, depth: str = "comprehensive") -> str:
        """Guide for conducting web research on a topic."""
        if depth == "quick":
            return f"""I need to research "{topic}" quickly. Please:

1. Use rival_retrieve with search:"{topic}" to find relevant sources
2. Follow up with 2-3 key sources using rival_retrieve 
3. Summarize key findings and provide sources

Keep the research focused and concise."""
        
        elif depth == "comprehensive":
            return f"""I need comprehensive research on "{topic}". Please:

1. Start with rival_retrieve using search:"{topic}" to identify key sources
2. Use research_website on the most promising sources (max_pages=8-12)
3. Store findings with store_data=True for future reference
4. Use search_nodes to cross-reference information
5. Provide a detailed analysis with multiple perspectives

Take your time to gather thorough information."""
        
        else:  # deep
            return f"""I need deep, expert-level research on "{topic}". Please:

1. Begin with multiple search queries using rival_retrieve with search:"{topic}"
2. Use research_website on 3-4 authoritative sources (max_pages=15+ each)
3. Use explore_docs if technical documentation is relevant
4. Store all data with store_data=True
5. Use adaptive_reason to analyze findings step-by-step
6. Cross-reference with search_nodes queries
7. Provide expert-level analysis with evidence and source citations

This is for serious research - be thorough and methodical."""


    @mcp.prompt("documentation-explorer")
    def documentation_explorer_prompt(framework_or_api: str) -> str:
        """Guide for exploring technical documentation comprehensively."""
        return f"""I need to understand "{framework_or_api}" documentation thoroughly. Please:

1. Start with rival_retrieve to get the main documentation page
2. Use explore_docs with max_pages=20-30 to systematically explore
3. Focus on these key areas:
   - Getting started / quickstart
   - API reference
   - Examples and tutorials
   - Best practices
4. Store key information with store_data=True
5. Provide a structured overview covering:
   - Core concepts
   - Key features
   - Usage patterns
   - Important APIs
   - Example implementations

Make this a complete technical reference."""


    @mcp.prompt("competitive-analysis")
    def competitive_analysis_prompt(company_or_product: str) -> str:
        """Guide for conducting competitive analysis of companies or products."""
        return f"""I need a competitive analysis of "{company_or_product}". Please:

1. Use map_website to understand their site structure and offerings
2. Use research_website on key product/service pages (max_pages=10-15)
3. Look for:
   - Product features and positioning
   - Pricing information
   - Target market
   - Technology stack (if relevant)
   - Company background
4. Store findings with store_data=True
5. Provide analysis covering:
   - Strengths and differentiators
   - Market positioning
   - Key offerings
   - Potential weaknesses or gaps
   - Strategic insights

Be thorough but respectful of their content."""


    @mcp.prompt("research-synthesis")
    def research_synthesis_prompt(topic: str) -> str:
        """Multi-step prompt for synthesizing research from stored data."""
        return f"""I've gathered research on '{topic}' and need to synthesize findings.

Please help me synthesize this research by:

1. Use search_nodes with queries related to '{topic}'
2. Use get_full_store to see all available data
3. Use adaptive_reason to analyze patterns and connections
4. Provide a comprehensive synthesis with key insights

Look for:
- Common themes and patterns
- Contradictions or conflicting information
- Key insights and conclusions
- Evidence strength and source quality
- Knowledge gaps that need more research

Provide a well-structured synthesis that combines all findings."""


    @mcp.prompt("web-extraction")
    def web_extraction_prompt(url: str, extraction_goal: str) -> str:
        """Guide for extracting specific information from web content."""
        return f"""I need to extract specific information from {url}.

Goal: {extraction_goal}

Please:
1. Use rival_retrieve to get the content from {url}
2. If the content seems incomplete or you need more context:
   - Try with traverse_links=True and max_depth=1 to get related pages
   - Or use research_website if it's part of a larger site
3. Extract the requested information focusing on:
   - Accuracy and completeness
   - Proper attribution
   - Relevant context
4. If storing for later use, set store_data=True

Provide clear, well-structured results."""


    @mcp.prompt("problem-solving")
    def problem_solving_prompt(problem: str) -> str:
        """Guide for systematic problem-solving with research and reasoning."""
        return f"""I need help solving this problem: "{problem}"

Please approach this systematically:

1. **Research Phase:**
   - Use rival_retrieve with relevant search queries
   - Gather information from authoritative sources
   - Store key findings with store_data=True

2. **Analysis Phase:**
   - Use adaptive_reason to break down the problem step-by-step
   - Consider multiple approaches and solutions
   - Identify key constraints and requirements

3. **Solution Phase:**
   - Synthesize research and reasoning into concrete solutions
   - Provide step-by-step implementation guidance
   - Include relevant examples and best practices

4. **Validation:**
   - Cross-reference with search_nodes for additional insights
   - Ensure solution addresses all aspects of the problem

Be thorough, analytical, and practical."""


    @mcp.prompt("code-research")
    def code_research_prompt(technology: str, use_case: str) -> str:
        """Guide for researching code examples and implementation patterns."""
        return f"""I need to research how to implement {use_case} using {technology}.

Please:

1. **Documentation Research:**
   - Use explore_docs on official {technology} documentation
   - Focus on relevant APIs and examples
   - Look for best practices and patterns

2. **Example Gathering:**
   - Use rival_retrieve to search for: "search:{technology} {use_case} examples"
   - Look for tutorial content and code repositories
   - Use research_website on promising sources

3. **Pattern Analysis:**
   - Store code examples and patterns with store_data=True
   - Use adaptive_reason to analyze different approaches
   - Identify common patterns and best practices

4. **Implementation Guide:**
   - Provide step-by-step implementation guidance
   - Include code examples and explanations
   - Highlight potential pitfalls and solutions

Focus on practical, working examples with clear explanations."""


    @mcp.prompt("fact-checking")
    def fact_checking_prompt(claim: str) -> str:
        """Guide for fact-checking claims using multiple sources."""
        return f"""I need to fact-check this claim: "{claim}"

Please conduct thorough verification:

1. **Source Gathering:**
   - Use rival_retrieve with multiple search queries
   - Look for authoritative sources (academic, official, reputable news)
   - Gather diverse perspectives

2. **Cross-Verification:**
   - Use research_website on 2-3 authoritative sources
   - Store findings with store_data=True
   - Look for consensus or contradictions

3. **Evidence Analysis:**
   - Use adaptive_reason to evaluate evidence quality
   - Consider source credibility and potential bias
   - Look for primary vs secondary sources

4. **Conclusion:**
   - Provide clear assessment: Verified/Disputed/Unclear
   - Present supporting evidence
   - Note any limitations or caveats
   - Include source citations

Be objective and thorough in verification."""