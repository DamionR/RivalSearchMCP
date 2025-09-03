#!/usr/bin/env python3
"""
Data models for Google Search engine.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .base import BaseSearchResult, BaseSearchMetadata


@dataclass
class GoogleSearchResult(BaseSearchResult):
    """Represents a Google Search result."""

    engine: str = "google"
    domain: str = ""
    google_id: str = ""
    google_category: str = ""
    google_related_searches: List[str] = field(default_factory=list)
    google_instant_answer: str = ""
    google_news_category: str = ""
    google_video_duration: str = ""
    google_image_dimensions: str = ""
    google_sitelinks: List[str] = field(default_factory=list)
    google_featured_snippet: str = ""
    
    def __post_init__(self):
        """Initialize computed fields after dataclass creation."""
        super().__post_init__()
        if not self.domain:
            self.domain = self.extract_domain(self.url)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        google_dict = {
            "domain": self.domain,
            "google_id": self.google_id,
            "google_category": self.google_category,
            "google_related_searches": self.google_related_searches,
            "google_instant_answer": self.google_instant_answer,
            "google_news_category": self.google_news_category,
            "google_video_duration": self.google_video_duration,
            "google_image_dimensions": self.google_image_dimensions,
            "google_sitelinks": self.google_sitelinks,
            "google_featured_snippet": self.google_featured_snippet,
        }
        base_dict.update(google_dict)
        return base_dict


@dataclass
class GoogleSearchMetadata(BaseSearchMetadata):
    """Metadata for Google search operations."""
    
    engine: str = "google"
    google_region: str = "US"
    google_language: str = "en"
    google_safe_search: str = "moderate"
    google_count: int = 0
    google_start: int = 0
    google_total_results: int = 0
    google_search_time: float = 0.0
    google_has_instant_answer: bool = False
    google_has_featured_snippet: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        google_dict = {
            "google_region": self.google_region,
            "google_language": self.google_language,
            "google_safe_search": self.google_safe_search,
            "google_count": self.google_count,
            "google_start": self.google_start,
            "google_total_results": self.google_total_results,
            "google_search_time": self.google_search_time,
            "google_has_instant_answer": self.google_has_instant_answer,
            "google_has_featured_snippet": self.google_has_featured_snippet,
        }
        base_dict.update(google_dict)
        return google_dict


@dataclass
class GoogleNewsResult(GoogleSearchResult):
    """Represents a Google News result."""
    
    google_news_source: str = ""
    google_news_date: str = ""
    google_news_author: str = ""
    google_news_location: str = ""
    google_news_category: str = ""
    google_news_summary: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        news_dict = {
            "google_news_source": self.google_news_source,
            "google_news_date": self.google_news_date,
            "google_news_author": self.google_news_author,
            "google_news_location": self.google_news_location,
            "google_news_summary": self.google_news_summary,
        }
        base_dict.update(news_dict)
        return base_dict


@dataclass
class GoogleVideoResult(GoogleSearchResult):
    """Represents a Google Video result."""
    
    google_video_duration: str = ""
    google_video_thumbnail: str = ""
    google_video_views: str = ""
    google_video_upload_date: str = ""
    google_video_publisher: str = ""
    google_video_quality: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        video_dict = {
            "google_video_thumbnail": self.google_video_thumbnail,
            "google_video_views": self.google_video_views,
            "google_video_upload_date": self.google_video_upload_date,
            "google_video_publisher": self.google_video_publisher,
            "google_video_quality": self.google_video_quality,
        }
        base_dict.update(video_dict)
        return base_dict


@dataclass
class GoogleImageResult(GoogleSearchResult):
    """Represents a Google Image result."""
    
    google_image_dimensions: str = ""
    google_image_thumbnail: str = ""
    google_image_source_page: str = ""
    google_image_license: str = ""
    google_image_type: str = ""
    google_image_size: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        image_dict = {
            "google_image_thumbnail": self.google_image_thumbnail,
            "google_image_source_page": self.google_image_source_page,
            "google_image_license": self.google_image_license,
            "google_image_type": self.google_image_type,
            "google_image_size": self.google_image_size,
        }
        base_dict.update(image_dict)
        return base_dict
