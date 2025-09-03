"""
LLMs.txt Generator schemas for RivalSearchMCP.
Structured data models for LLMs.txt generation and documentation.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PageData(BaseModel):
    """Individual page data for LLMs.txt generation."""

    url: str = Field(description="Page URL")
    title: str = Field(description="Page title")
    content: str = Field(description="Page content")
    category: str = Field(description="Page category")
    description: str = Field(description="Page description")
    source: str = Field(default="link_discovery", description="Discovery source")


class LLMsGenerationConfig(BaseModel):
    """Configuration for LLMs.txt generation."""

    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    urls: List[str] = Field(description="List of URLs to start crawling from")
    output_dir: str = Field(
        default=".", description="Output directory for generated files"
    )
    max_pages: int = Field(
        default=100, description="Maximum number of pages to process"
    )
    max_depth: int = Field(default=3, description="Maximum depth for crawling")
    traversal_mode: str = Field(
        default="docs", description="Traversal mode (docs, research, map)"
    )
    rate_limit: float = Field(
        default=1.0, description="Delay between requests in seconds"
    )
    user_agent: str = Field(
        default="LLMs.txt Generator/1.0", description="User agent string"
    )
    content_selectors: Optional[List[str]] = Field(
        default=None, description="CSS selectors for content extraction"
    )
    title_selectors: Optional[List[str]] = Field(
        default=None, description="CSS selectors for title extraction"
    )
    category_rules: Optional[Dict[str, List[str]]] = Field(
        default=None, description="Rules for categorizing pages"
    )


class LLMsGenerationResult(BaseModel):
    """Result of LLMs.txt generation process."""

    success: bool = Field(description="Whether generation was successful")
    pages_processed: int = Field(description="Number of pages processed")
    files_generated: List[str] = Field(description="List of generated files")
    output_directory: str = Field(description="Directory where files were saved")
    files_content: Dict[str, str] = Field(description="Content of generated files")
    categories_found: List[str] = Field(
        description="Categories discovered during processing"
    )
    total_content_length: int = Field(description="Total content length processed")
    processing_time: Optional[float] = Field(
        default=None, description="Processing time in seconds"
    )


class LLMsFileContent(BaseModel):
    """Content structure for LLMs.txt files."""

    project_title: str = Field(description="Project title")
    project_description: str = Field(description="Project description")
    sections: Dict[str, List[PageData]] = Field(
        description="Pages organized by category"
    )
    total_pages: int = Field(description="Total number of pages")
    generation_date: str = Field(description="Generation timestamp")
    source_urls: List[str] = Field(description="Source URLs used for generation")


class LLMsCategorizationRule(BaseModel):
    """Rule for categorizing pages in LLMs.txt generation."""

    category: str = Field(description="Category name")
    keywords: List[str] = Field(description="Keywords that indicate this category")
    priority: int = Field(
        default=1, description="Priority for matching (higher = more specific)"
    )
    description: str = Field(description="Category description")


class LLMsTraversalStats(BaseModel):
    """Statistics for website traversal during LLMs.txt generation."""

    total_urls_discovered: int = Field(description="Total URLs discovered")
    urls_processed: int = Field(description="URLs successfully processed")
    urls_failed: int = Field(description="URLs that failed to process")
    average_content_length: float = Field(description="Average content length per page")
    categories_distribution: Dict[str, int] = Field(
        description="Distribution of pages across categories"
    )
    processing_errors: List[str] = Field(
        description="List of processing errors encountered"
    )
    start_time: str = Field(description="Traversal start time")
    end_time: str = Field(description="Traversal end time")


class LLMsExportFormat(BaseModel):
    """Export format configuration for LLMs.txt generation."""

    format_type: str = Field(description="Export format (txt, json, xml)")
    include_optional: bool = Field(default=True, description="Include optional section")
    include_metadata: bool = Field(default=True, description="Include metadata")
    content_format: str = Field(
        default="full", description="Content format (full, summary, links_only)"
    )
    file_extension: str = Field(description="File extension for the format")
    encoding: str = Field(default="utf-8", description="File encoding")


class LLMsQualityMetrics(BaseModel):
    """Quality metrics for generated LLMs.txt files."""

    content_coverage: float = Field(description="Percentage of content covered")
    category_balance: float = Field(description="Balance of content across categories")
    link_validity: float = Field(description="Percentage of valid links")
    content_quality: float = Field(description="Overall content quality score")
    structure_consistency: float = Field(
        description="Consistency of document structure"
    )
    compliance_score: float = Field(
        description="Compliance with llmstxt.org specification"
    )
    readability_score: float = Field(description="Content readability score")
    completeness_score: float = Field(description="Overall completeness score")
