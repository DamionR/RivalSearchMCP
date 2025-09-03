#!/usr/bin/env python3
"""
Data models for Yahoo Search engine.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .base import BaseSearchResult, BaseSearchMetadata


@dataclass
class YahooSearchResult(BaseSearchResult):
    """Represents a Yahoo Search result."""
    
    engine: str = "yahoo"
    yahoo_id: str = ""
    yahoo_category: str = ""
    yahoo_related_searches: List[str] = field(default_factory=list)
    yahoo_instant_answer: str = ""
    yahoo_news_category: str = ""
    yahoo_video_duration: str = ""
    yahoo_image_dimensions: str = ""
    yahoo_sponsored: bool = False
    yahoo_news_source: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        yahoo_dict = {
            "yahoo_id": self.yahoo_id,
            "yahoo_category": self.yahoo_category,
            "yahoo_related_searches": self.yahoo_related_searches,
            "yahoo_instant_answer": self.yahoo_instant_answer,
            "yahoo_news_category": self.yahoo_news_category,
            "yahoo_video_duration": self.yahoo_video_duration,
            "yahoo_image_dimensions": self.yahoo_image_dimensions,
            "yahoo_sponsored": self.yahoo_sponsored,
            "yahoo_news_source": self.yahoo_news_source,
        }
        base_dict.update(yahoo_dict)
        return base_dict


@dataclass
class YahooSearchMetadata(BaseSearchMetadata):
    """Metadata for Yahoo search operations."""
    
    engine: str = "yahoo"
    yahoo_region: str = "US"
    yahoo_language: str = "en"
    yahoo_safe_search: str = "moderate"
    yahoo_count: int = 0
    yahoo_start: int = 0
    yahoo_total_results: int = 0
    yahoo_search_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        yahoo_dict = {
            "yahoo_region": self.yahoo_region,
            "yahoo_language": self.yahoo_language,
            "yahoo_safe_search": self.yahoo_safe_search,
            "yahoo_count": self.yahoo_count,
            "yahoo_start": self.yahoo_start,
            "yahoo_total_results": self.yahoo_total_results,
            "yahoo_search_time": self.yahoo_search_time,
        }
        base_dict.update(yahoo_dict)
        return yahoo_dict


@dataclass
class YahooNewsResult(YahooSearchResult):
    """Represents a Yahoo News result."""
    
    yahoo_news_source: str = ""
    yahoo_news_date: str = ""
    yahoo_news_author: str = ""
    yahoo_news_location: str = ""
    yahoo_news_category: str = ""
    yahoo_news_summary: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        news_dict = {
            "yahoo_news_summary": self.yahoo_news_summary,
        }
        base_dict.update(news_dict)
        return base_dict


@dataclass
class YahooVideoResult(YahooSearchResult):
    """Represents a Yahoo Video result."""
    
    yahoo_video_duration: str = ""
    yahoo_video_thumbnail: str = ""
    yahoo_video_views: str = ""
    yahoo_video_upload_date: str = ""
    yahoo_video_publisher: str = ""
    yahoo_video_quality: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        video_dict = {
            "yahoo_video_thumbnail": self.yahoo_video_thumbnail,
            "yahoo_video_views": self.yahoo_video_views,
            "yahoo_video_upload_date": self.yahoo_video_upload_date,
            "yahoo_video_publisher": self.yahoo_video_publisher,
            "yahoo_video_quality": self.yahoo_video_quality,
        }
        base_dict.update(video_dict)
        return base_dict


@dataclass
class YahooImageResult(YahooSearchResult):
    """Represents a Yahoo Image result."""
    
    yahoo_image_dimensions: str = ""
    yahoo_image_thumbnail: str = ""
    yahoo_image_source_page: str = ""
    yahoo_image_license: str = ""
    yahoo_image_type: str = ""
    yahoo_image_size: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        image_dict = {
            "yahoo_image_thumbnail": self.yahoo_image_thumbnail,
            "yahoo_image_source_page": self.yahoo_image_source_page,
            "yahoo_image_license": self.yahoo_image_license,
            "yahoo_image_type": self.yahoo_image_type,
            "yahoo_image_size": self.yahoo_image_size,
        }
        base_dict.update(image_dict)
        return base_dict
