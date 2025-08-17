"""
Structured output schemas for FastMCP migration.
These models provide type-safe, validated outputs while maintaining compatibility.
"""

from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field


# ===== SEARCH & RETRIEVAL SCHEMAS =====

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


# ===== REASONING SCHEMAS =====

class ReasoningStep(BaseModel):
    """A single reasoning step."""
    step_num: int = Field(description="Step number")
    content: str = Field(description="Step content")
    estimated_steps: int = Field(description="Total estimated steps")
    continue_reasoning: bool = Field(description="Whether to continue reasoning")
    is_revision: bool = Field(default=False, description="Whether this is a revision")
    revises_step: Optional[int] = Field(default=None, description="Step being revised")
    branch_from_step: Optional[int] = Field(default=None, description="Step to branch from")
    branch_id: Optional[str] = Field(default=None, description="Branch identifier")
    needs_more_steps: bool = Field(default=False, description="Whether more steps needed")


class ReasoningResult(BaseModel):
    """Result from adaptive_reason tool."""
    current_step: ReasoningStep = Field(description="Current reasoning step")
    paths: List[str] = Field(description="Available reasoning paths")
    steps_count: int = Field(description="Total steps processed")


# ===== DATA STORE SCHEMAS =====

class Node(BaseModel):
    """A node in the knowledge graph."""
    name: str = Field(description="Node name/identifier")
    type: str = Field(description="Node type")
    facts: List[str] = Field(description="Facts associated with this node")


class Link(BaseModel):
    """A relationship between two nodes."""
    from_node: str = Field(alias="from", description="Source node name")
    to_node: str = Field(alias="to", description="Target node name")
    relation: str = Field(description="Relationship type")


class GraphData(BaseModel):
    """Complete graph data structure."""
    nodes: List[Node] = Field(description="All nodes in the graph")
    links: List[Link] = Field(description="All links in the graph")


class NodeOperationResult(BaseModel):
    """Result of node add/remove operations."""
    success: bool = Field(description="Whether operation was successful")
    affected_nodes: List[str] = Field(description="Names of affected nodes")
    operation: str = Field(description="Operation performed (add/remove)")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional operation details")


class FactOperationResult(BaseModel):
    """Result of fact add/remove operations."""
    success: bool = Field(description="Whether operation was successful")
    affected_facts: Dict[str, List[str]] = Field(description="Facts affected per node")
    operation: str = Field(description="Operation performed (add/remove)")


class LinkOperationResult(BaseModel):
    """Result of link add/remove operations."""
    success: bool = Field(description="Whether operation was successful")
    affected_links: List[Dict[str, str]] = Field(description="Links affected")
    operation: str = Field(description="Operation performed (add/remove)")


class SearchNodesResult(BaseModel):
    """Result of node search operations."""
    success: bool = Field(description="Whether search was successful")
    query: str = Field(description="Search query used")
    nodes: List[Node] = Field(description="Matching nodes")
    links: List[Link] = Field(description="Links between matching nodes")
    total_matches: int = Field(description="Total number of matching nodes")


# ===== DATA STORE RESULT SCHEMA =====

class DataStoreResult(BaseModel):
    """Result from data store operations."""
    success: bool = Field(description="Whether operation was successful")
    operation: str = Field(description="Type of operation performed")
    affected_count: int = Field(description="Number of items affected")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Operation result data")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")


# ===== SUCCESS RESPONSE SCHEMA =====

class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool = Field(default=True, description="Operation success")
    message: str = Field(description="Success message")


# ===== WEB TOOLS SCHEMAS =====

class GoogleSearchResult(BaseModel):
    """Result from Google search operation."""
    success: bool = Field(description="Whether search was successful")
    results: List[SearchResult] = Field(description="List of search results")
    query: str = Field(description="Search query used")
    count: int = Field(description="Number of results returned")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class WebsiteTraversalResult(BaseModel):
    """Result from website traversal operation."""
    success: bool = Field(description="Whether traversal was successful")
    pages: List[TraversalPage] = Field(description="List of traversed pages")
    summary: str = Field(description="Human-readable summary")
    total_pages: int = Field(description="Total number of pages")
    source: str = Field(description="Source URL")