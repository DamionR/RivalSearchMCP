"""
Web tools schemas for FastMCP server.
Handles Google search results, search scraping, and website traversal operations.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from .retrieval_schemas import SearchResult, TraversalPage


class GoogleSearchResult(BaseModel):
    """Result from Google search operation."""
    success: bool = Field(description="Whether search was successful")
    results: List[SearchResult] = Field(description="List of search results")
    query: str = Field(description="Search query used")
    count: int = Field(description="Number of results returned")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class GoogleSearchScrapeResult(BaseModel):
    """Result from Google Search scraping operation."""
    success: bool = Field(description="Whether scraping was successful")
    results: List[Dict[str, Any]] = Field(description="List of scraped search results")
    query: str = Field(description="Search query used")
    count: int = Field(description="Number of results returned")
    total_results: int = Field(description="Total results found")
    search_metadata: Dict[str, Any] = Field(default={}, description="Search metadata")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class WebsiteTraversalResult(BaseModel):
    """Result from website traversal operation."""
    success: bool = Field(description="Whether traversal was successful")
    pages: List[TraversalPage] = Field(description="List of traversed pages")
    summary: str = Field(description="Human-readable summary")
    total_pages: int = Field(description="Total number of pages")
    source: str = Field(description="Source URL")
