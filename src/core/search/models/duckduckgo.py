#!/usr/bin/env python3
"""
Data models for DuckDuckGo Search engine.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .base import BaseSearchResult, BaseSearchMetadata


@dataclass
class DuckDuckGoSearchResult(BaseSearchResult):
    """Represents a DuckDuckGo Search result."""
    
    engine: str = "duckduckgo"
    ddg_id: str = ""
    ddg_category: str = ""
    ddg_related_topics: List[str] = field(default_factory=list)
    ddg_instant_answer: str = ""
    ddg_abstract_source: str = ""
    ddg_abstract_url: str = ""
    ddg_related_searches: List[str] = field(default_factory=list)
    ddg_answer_box: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        ddg_dict = {
            "ddg_id": self.ddg_id,
            "ddg_category": self.ddg_category,
            "ddg_related_topics": self.ddg_related_topics,
            "ddg_instant_answer": self.ddg_instant_answer,
            "ddg_abstract_source": self.ddg_abstract_source,
            "ddg_abstract_url": self.ddg_abstract_url,
            "ddg_related_searches": self.ddg_related_searches,
            "ddg_answer_box": self.ddg_answer_box,
        }
        base_dict.update(ddg_dict)
        return base_dict


@dataclass
class DuckDuckGoSearchMetadata(BaseSearchMetadata):
    """Metadata for DuckDuckGo search operations."""
    
    engine: str = "duckduckgo"
    ddg_region: str = "us-en"
    ddg_safe_search: str = "moderate"
    ddg_time: str = ""
    ddg_type: str = "text"
    ddg_has_instant_answer: bool = False
    ddg_has_answer_box: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        ddg_dict = {
            "ddg_region": self.ddg_region,
            "ddg_safe_search": self.ddg_safe_search,
            "ddg_time": self.ddg_time,
            "ddg_type": self.ddg_type,
            "ddg_has_instant_answer": self.ddg_has_instant_answer,
            "ddg_has_answer_box": self.ddg_has_answer_box,
        }
        base_dict.update(ddg_dict)
        return ddg_dict


@dataclass
class DuckDuckGoInstantAnswer(BaseSearchResult):
    """Represents a DuckDuckGo Instant Answer."""
    
    engine: str = "duckduckgo"
    ddg_abstract: str = ""
    ddg_abstract_source: str = ""
    ddg_abstract_url: str = ""
    ddg_answer: str = ""
    ddg_answer_type: str = ""
    ddg_definition: str = ""
    ddg_definition_source: str = ""
    ddg_definition_url: str = ""
    ddg_image: str = ""
    ddg_redirect: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        instant_dict = {
            "ddg_abstract": self.ddg_abstract,
            "ddg_abstract_source": self.ddg_abstract_source,
            "ddg_abstract_url": self.ddg_abstract_url,
            "ddg_answer": self.ddg_answer,
            "ddg_answer_type": self.ddg_answer_type,
            "ddg_definition": self.ddg_definition,
            "ddg_definition_source": self.ddg_definition_source,
            "ddg_definition_url": self.ddg_definition_url,
            "ddg_image": self.ddg_image,
            "ddg_redirect": self.ddg_redirect,
        }
        base_dict.update(instant_dict)
        return base_dict


@dataclass
class DuckDuckGoRelatedTopic(BaseSearchResult):
    """Represents a DuckDuckGo Related Topic."""
    
    engine: str = "duckduckgo"
    ddg_topic: str = ""
    ddg_first_url: str = ""
    ddg_text: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        base_dict = super().to_dict()
        topic_dict = {
            "ddg_topic": self.ddg_topic,
            "ddg_first_url": self.ddg_first_url,
            "ddg_text": self.ddg_text,
        }
        base_dict.update(topic_dict)
        return base_dict
