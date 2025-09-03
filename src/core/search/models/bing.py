#!/usr/bin/env python3
"""
Data models for Bing Search engine.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .base import BaseSearchResult, BaseSearchMetadata


@dataclass
class BingSearchResult(BaseSearchResult):
    """Represents a Bing Search result."""
    
    engine: str = "bing"
    bing_id: str = ""
    bing_position: int = 0
    bing_category: str = ""
    bing_related_searches: List[str] = field(default_factory=list)
    bing_instant_answer: str = ""
    bing_news_category: str = ""
    bing_video_duration: str = ""
    bing_image_dimensions: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        bing_dict = {
            "bing_id": self.bing_id,
            "bing_position": self.bing_position,
            "bing_category": self.bing_category,
            "bing_related_searches": self.bing_related_searches,
            "bing_instant_answer": self.bing_instant_answer,
            "bing_news_category": self.bing_news_category,
            "bing_video_duration": self.bing_video_duration,
            "bing_image_dimensions": self.bing_image_dimensions,
        }
        base_dict.update(bing_dict)
        return base_dict


@dataclass
class BingSearchMetadata(BaseSearchMetadata):
    """Metadata for Bing search operations."""
    
    engine: str = "bing"
    bing_region: str = "en-US"
    bing_market: str = "en-US"
    bing_safe_search: str = "moderate"
    bing_count: int = 0
    bing_offset: int = 0
    bing_total_estimated_matches: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        bing_dict = {
            "bing_region": self.bing_region,
            "bing_market": self.bing_market,
            "bing_safe_search": self.bing_safe_search,
            "bing_count": self.bing_count,
            "bing_offset": self.bing_offset,
            "bing_total_estimated_matches": self.bing_total_estimated_matches,
        }
        base_dict.update(bing_dict)
        return bing_dict


@dataclass
class BingNewsResult(BingSearchResult):
    """Represents a Bing News result."""
    
    bing_news_category: str = ""
    bing_news_source: str = ""
    bing_news_date: str = ""
    bing_news_author: str = ""
    bing_news_location: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        news_dict = {
            "bing_news_source": self.bing_news_source,
            "bing_news_date": self.bing_news_date,
            "bing_news_author": self.bing_news_author,
            "bing_news_location": self.bing_news_location,
        }
        base_dict.update(news_dict)
        return base_dict


@dataclass
class BingVideoResult(BingSearchResult):
    """Represents a Bing Video result."""
    
    bing_video_duration: str = ""
    bing_video_thumbnail: str = ""
    bing_video_views: str = ""
    bing_video_upload_date: str = ""
    bing_video_publisher: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        video_dict = {
            "bing_video_thumbnail": self.bing_video_thumbnail,
            "bing_video_views": self.bing_video_views,
            "bing_video_upload_date": self.bing_video_upload_date,
            "bing_video_publisher": self.bing_video_publisher,
        }
        base_dict.update(video_dict)
        return base_dict


@dataclass
class BingImageResult(BingSearchResult):
    """Represents a Bing Image result."""
    
    bing_image_dimensions: str = ""
    bing_image_thumbnail: str = ""
    bing_image_source_page: str = ""
    bing_image_license: str = ""
    bing_image_type: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        image_dict = {
            "bing_image_thumbnail": self.bing_image_thumbnail,
            "bing_image_source_page": self.bing_image_source_page,
            "bing_image_license": self.bing_image_license,
            "bing_image_type": self.bing_image_type,
        }
        base_dict.update(image_dict)
        return base_dict
