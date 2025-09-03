"""
Schemas package for RivalSearchMCP.
Data models and validation schemas for all components.
"""

from .common import SuccessResponse
from .llms import (
    LLMsCategorizationRule,
    LLMsExportFormat,
    LLMsFileContent,
    LLMsGenerationConfig,
    LLMsGenerationResult,
    LLMsQualityMetrics,
    LLMsTraversalStats,
    PageData,
)

# Import all schemas from componentized modules
from .retrieval import (
    RetrieveResult,
    SearchResult,
    StreamResult,
    TraversalPage,
    TraversalResult,
    WebContent,
)

# Import new schemas
from .trends import (
    ComparisonResult,
    ExportResult,
    RegionInterest,
    RelatedQuery,
    SQLTableResult,
    TrendData,
    TrendsComparisonRequest,
    TrendsExportRequest,
    TrendsSearchRequest,
)
from .web import (
    GoogleSearchResult,
    GoogleSearchScrapeResult,
    WebsiteTraversalResult,
)

__all__ = [
    # Core schemas
    "SearchResult",
    "WebContent",
    "TraversalPage",
    "TraversalResult",
    "RetrieveResult",
    "StreamResult",
    "GoogleSearchResult",
    "GoogleSearchScrapeResult",
    "WebsiteTraversalResult",
    "SuccessResponse",
    # Google Trends schemas
    "TrendData",
    "RelatedQuery",
    "RegionInterest",
    "ExportResult",
    "SQLTableResult",
    "ComparisonResult",
    "TrendsSearchRequest",
    "TrendsExportRequest",
    "TrendsComparisonRequest",
    # LLMs.txt Generator schemas
    "PageData",
    "LLMsGenerationConfig",
    "LLMsGenerationResult",
    "LLMsFileContent",
    "LLMsCategorizationRule",
    "LLMsTraversalStats",
    "LLMsExportFormat",
    "LLMsQualityMetrics",
]
