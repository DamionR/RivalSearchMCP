#!/usr/bin/env python3
"""
Data models for Google Search scraper.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
from urllib.parse import urlparse


@dataclass
class GoogleSearchResult:
    """Represents a Google Search result."""
    url: str
    title: str
    description: str
    position: int = 0
    domain: str = ""
    timestamp: str = ""
    content_hash: str = ""
    search_snippet: str = ""
    search_position: int = 0
    is_organic: bool = True
    has_rich_snippet: bool = False
    rich_snippet_type: str = ""
    estimated_traffic: str = ""
    search_features: Optional[List[str]] = None
    
    def __post_init__(self):
        """Initialize computed fields after dataclass creation."""
        if not self.domain:
            self.domain = self.extract_domain(self.url)
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'domain': self.domain,
            'position': self.position,
            'timestamp': self.timestamp,
            'content_hash': self.content_hash,
            'search_snippet': self.search_snippet,
            'search_position': self.search_position,
            'is_organic': self.is_organic,
            'has_rich_snippet': self.has_rich_snippet,
            'rich_snippet_type': self.rich_snippet_type,
            'estimated_traffic': self.estimated_traffic,
            'search_features': self.search_features
        }
    
    def __repr__(self) -> str:
        return f"GoogleSearchResult(url={self.url}, title={self.title}, domain={self.domain}, position={self.position})"
