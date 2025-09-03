#!/usr/bin/env python3
"""
Base data models for all search engines.
"""

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse


@dataclass
class BaseSearchResult(ABC):
    """Base class for all search engine results."""
    
    url: str
    title: str
    description: str
    position: int = 0
    engine: str = ""
    timestamp: str = ""
    content_hash: str = ""
    search_snippet: str = ""
    search_position: int = 0
    is_organic: bool = True
    has_rich_snippet: bool = False
    rich_snippet_type: str = ""
    estimated_traffic: str = ""
    search_features: Optional[List[str]] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize computed fields after dataclass creation."""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.content_hash:
            self.content_hash = hashlib.md5(self.url.encode()).hexdigest()
        if not self.search_snippet:
            self.search_snippet = self.description
        if not self.search_position:
            self.search_position = self.position
        if self.search_features is None:
            self.search_features = []
    
    def extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            return urlparse(url).netloc
        except:
            return "unknown"
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization. Must be implemented by subclasses."""
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(url={self.url}, title={self.title}, engine={self.engine}, position={self.position})"


@dataclass
class BaseSearchMetadata:
    """Base metadata for search operations."""
    
    query: str
    engine: str
    timestamp: str = ""
    total_results: int = 0
    search_time_ms: float = 0.0
    success: bool = True
    error_message: str = ""
    
    def __post_init__(self):
        """Initialize computed fields after dataclass creation."""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "query": self.query,
            "engine": self.engine,
            "timestamp": self.timestamp,
            "total_results": self.total_results,
            "search_time_ms": self.search_time_ms,
            "success": self.success,
            "error_message": self.error_message,
        }


@dataclass
class BaseSearchRequest:
    """Base request model for search operations."""
    
    query: str
    num_results: int = 10
    extract_content: bool = False
    follow_links: bool = False
    max_depth: int = 1
    use_fallback: bool = True
    timeout: int = 30
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "query": self.query,
            "num_results": self.num_results,
            "extract_content": self.extract_content,
            "follow_links": self.follow_links,
            "max_depth": self.max_depth,
            "use_fallback": self.use_fallback,
            "timeout": self.timeout,
        }
