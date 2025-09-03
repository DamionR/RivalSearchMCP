"""
Google Trends schemas for RivalSearchMCP.
Structured data models for Google Trends API responses.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TrendData(BaseModel):
    """Structured trend data response."""

    keyword: str = Field(description="Search keyword")
    mean_interest: float = Field(description="Average interest over time")
    peak_interest: int = Field(description="Peak interest value")
    peak_date: str = Field(description="Date of peak interest")
    data_points: int = Field(description="Number of data points")
    date_range: str = Field(description="Date range of data")


class RelatedQuery(BaseModel):
    """Related query information."""

    query: str = Field(description="Related search query")
    value: int = Field(description="Interest value")
    type: str = Field(description="Type: 'top' or 'rising'")


class RegionInterest(BaseModel):
    """Geographic interest data."""

    region: str = Field(description="Geographic region")
    interest: int = Field(description="Interest value")
    keyword: str = Field(description="Search keyword")


class ExportResult(BaseModel):
    """Export operation result."""

    filename: str = Field(description="Exported file name")
    format: str = Field(description="Export format")
    size_bytes: int = Field(description="File size in bytes")
    path: str = Field(description="Full file path")


class SQLTableResult(BaseModel):
    """SQL table creation result."""

    table_name: str = Field(description="Created table name")
    rows_inserted: int = Field(description="Number of rows inserted")
    columns: List[str] = Field(description="Table columns")
    database_path: str = Field(description="Database file path")


class ComparisonResult(BaseModel):
    """Comprehensive comparison result."""

    keywords: List[str] = Field(description="Keywords compared")
    timeframe: str = Field(description="Time range used")
    geo: str = Field(description="Geographic location")
    analysis_date: str = Field(description="Analysis timestamp")
    trends_data: List[TrendData] = Field(description="Trend analysis data")
    related_queries: Dict[str, List[RelatedQuery]] = Field(
        description="Related queries by keyword"
    )
    regional_interest: List[RegionInterest] = Field(
        description="Regional interest data"
    )
    summary: Dict[str, Any] = Field(description="Summary statistics")


class TrendsSearchRequest(BaseModel):
    """Request model for trends search."""

    keywords: List[str] = Field(description="List of search terms to analyze")
    timeframe: str = Field(default="today 12-m", description="Time range for data")
    geo: str = Field(default="US", description="Geographic location")
    resolution: str = Field(
        default="COUNTRY", description="Geographic resolution for regional data"
    )


class TrendsExportRequest(BaseModel):
    """Request model for trends export."""

    keywords: List[str] = Field(description="List of search terms")
    timeframe: str = Field(default="today 12-m", description="Time range for data")
    geo: str = Field(default="US", description="Geographic location")
    filename: Optional[str] = Field(
        default=None, description="Optional custom filename"
    )
    format: str = Field(default="csv", description="Export format (csv or json)")


class TrendsComparisonRequest(BaseModel):
    """Request model for comprehensive keyword comparison."""

    keywords: List[str] = Field(description="List of keywords to compare")
    timeframe: str = Field(default="today 12-m", description="Time range for analysis")
    geo: str = Field(default="US", description="Geographic location")
    include_related: bool = Field(
        default=True, description="Include related queries analysis"
    )
    include_regional: bool = Field(
        default=True, description="Include regional interest analysis"
    )
