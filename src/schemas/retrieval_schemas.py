"""
Retrieval schemas for FastMCP server.
Handles search results, web content, traversal pages, and retrieval operations.
"""

from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """Individual search result from Google search."""
    title: str = Field(description="Page title")
    link: str = Field(description="Page URL")
    snippet: str = Field(description="Content snippet")


class WebContent(BaseModel):
    """Content retrieved from a web page."""
    content: str = Field(description="Web page content")
    url: str = Field(description="Source URL")
    content_type: str = Field(default="text/html", description="Content type")
    ocr_text: List[str] = Field(default=[], description="Text extracted from images")
    images: List[Dict[str, Any]] = Field(default=[], description="Images found on the page")
    has_multimedia: bool = Field(default=False, description="Whether page contains multimedia content")


class TraversalPage(BaseModel):
    """A single page from link traversal."""
    url: str = Field(description="Page URL")
    title: str = Field(description="Page title")
    content: str = Field(description="Page content (truncated)")
    depth: int = Field(description="Traversal depth from start URL")


class TraversalResult(BaseModel):
    """Result from link traversal operation."""
    start_url: str = Field(description="Starting URL for traversal")
    pages_fetched: int = Field(description="Number of pages successfully fetched")
    total_attempts: int = Field(description="Total page fetch attempts")
    unique_links_found: int = Field(description="Total unique links discovered")
    max_depth_reached: int = Field(description="Maximum depth reached in traversal")
    pages: List[TraversalPage] = Field(description="List of fetched pages")
    summary: str = Field(description="Human-readable summary")
    config: Dict[str, Any] = Field(description="Configuration used for traversal")


class RetrieveResult(BaseModel):
    """Result from rival_retrieve tool."""
    success: bool = Field(description="Whether retrieval was successful")
    data: Union[List[SearchResult], WebContent, Dict[str, str], TraversalResult] = Field(description="Retrieved data")
    truncated: bool = Field(default=False, description="Whether content was truncated")
    remaining_bytes: int = Field(default=0, description="Remaining content length if truncated")
    original_url: str = Field(description="Original requested URL or search query")
    is_search: bool = Field(description="Whether this was a search query")
    is_traversal: bool = Field(default=False, description="Whether this was a link traversal")
    error_message: Optional[str] = Field(default=None, description="Error message if any")


class StreamResult(BaseModel):
    """Result from stream_retrieve tool."""
    success: bool = Field(description="Whether streaming was successful")
    content: str = Field(description="Streamed content")
    url: str = Field(description="WebSocket URL")
    chunks_received: int = Field(description="Number of chunks received")
