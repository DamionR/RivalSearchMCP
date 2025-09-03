#!/usr/bin/env python3
"""
MCP Pagination Support for RivalSearchMCP.
Implements cursor-based pagination for large result sets.
"""

import hashlib
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass, asdict

from src.logging.logger import logger


@dataclass
class PaginationCursor:
    """Cursor for MCP pagination."""
    timestamp: str
    page: int
    limit: int
    filters: Dict[str, Any]
    sort_order: str
    checksum: str
    
    def to_string(self) -> str:
        """Convert cursor to string representation."""
        cursor_data = {
            "timestamp": self.timestamp,
            "page": self.page,
            "limit": self.limit,
            "filters": self.filters,
            "sort_order": self.sort_order,
            "checksum": self.checksum
        }
        return json.dumps(cursor_data, sort_keys=True)


@dataclass
class PaginatedResponse:
    """Paginated response with cursor support."""
    items: List[Any]
    nextCursor: Optional[str] = None
    total_count: Optional[int] = None
    has_more: bool = False


class MCPPaginationManager:
    """Manages MCP pagination for various operations."""
    
    def __init__(self, default_limit: int = 50, max_limit: int = 1000):
        self.default_limit = default_limit
        self.max_limit = max_limit
        self.logger = logger
    
    def create_cursor(self, 
                     page: int = 1,
                     limit: Optional[int] = None,
                     filters: Optional[Dict[str, Any]] = None,
                     sort_order: str = "default") -> PaginationCursor:
        """Create a new pagination cursor."""
        if limit is None:
            limit = self.default_limit
        if filters is None:
            filters = {}
        
        # Validate limit
        limit = min(max(1, limit), self.max_limit)
        
        # Create checksum for stability
        cursor_data = f"{page}:{limit}:{json.dumps(filters, sort_keys=True)}:{sort_order}"
        checksum = hashlib.md5(cursor_data.encode()).hexdigest()
        
        return PaginationCursor(
            timestamp=datetime.now().isoformat(),
            page=page,
            limit=limit,
            filters=filters,
            sort_order=sort_order,
            checksum=checksum
        )
    
    def parse_cursor(self, cursor_string: str) -> Optional[PaginationCursor]:
        """Parse a cursor string back to PaginationCursor object."""
        try:
            cursor_data = json.loads(cursor_string)
            return PaginationCursor(**cursor_data)
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            self.logger.warning(f"Invalid cursor format: {e}")
            return None
    
    def validate_cursor(self, cursor: PaginationCursor) -> bool:
        """Validate cursor integrity and freshness."""
        try:
            # Check if cursor is too old (24 hours)
            cursor_time = datetime.fromisoformat(cursor.timestamp)
            if (datetime.now() - cursor_time).total_seconds() > 86400:  # 24 hours
                return False
            
            # Validate checksum
            cursor_data = f"{cursor.page}:{cursor.limit}:{json.dumps(cursor.filters, sort_keys=True)}:{cursor.sort_order}"
            expected_checksum = hashlib.md5(cursor_data.encode()).hexdigest()
            return cursor.checksum == expected_checksum
            
        except Exception as e:
            self.logger.error(f"Cursor validation failed: {e}")
            return False
    
    def paginate_resources_list(self, 
                               resources: List[Any],
                               cursor_string: Optional[str] = None,
                               limit: Optional[int] = None) -> PaginatedResponse:
        """Paginate resources/list operation."""
        return self._paginate_generic(
            items=resources,
            cursor_string=cursor_string,
            limit=limit,
            operation="resources/list"
        )
    
    def paginate_templates_list(self, 
                               templates: List[Any],
                               cursor_string: Optional[str] = None,
                               limit: Optional[int] = None) -> PaginatedResponse:
        """Paginate resources/templates/list operation."""
        return self._paginate_generic(
            items=templates,
            cursor_string=cursor_string,
            limit=limit,
            operation="resources/templates/list"
        )
    
    def paginate_prompts_list(self, 
                             prompts: List[Any],
                             cursor_string: Optional[str] = None,
                             limit: Optional[int] = None) -> PaginatedResponse:
        """Paginate prompts/list operation."""
        return self._paginate_generic(
            items=prompts,
            cursor_string=cursor_string,
            limit=limit,
            operation="prompts/list"
        )
    
    def paginate_tools_list(self, 
                           tools: List[Any],
                           cursor_string: Optional[str] = None,
                           limit: Optional[int] = None) -> PaginatedResponse:
        """Paginate tools/list operation."""
        return self._paginate_generic(
            items=tools,
            cursor_string=cursor_string,
            limit=limit,
            operation="tools/list"
        )
    
    def _paginate_generic(self, 
                          items: List[Any],
                          cursor_string: Optional[str] = None,
                          limit: Optional[int] = None,
                          operation: str = "unknown") -> PaginatedResponse:
        """Generic pagination logic."""
        try:
            # Parse cursor if provided
            current_cursor = None
            if cursor_string:
                current_cursor = self.parse_cursor(cursor_string)
                if not current_cursor or not self.validate_cursor(current_cursor):
                    self.logger.warning(f"Invalid cursor for {operation}, starting from beginning")
                    current_cursor = None
            
            # Set pagination parameters
            if current_cursor:
                page = current_cursor.page + 1
                page_limit = current_cursor.limit
                filters = current_cursor.filters
                sort_order = current_cursor.sort_order
            else:
                page = 1
                page_limit = limit or self.default_limit
                filters = {}
                sort_order = "default"
            
            # Validate and adjust limit
            page_limit = min(max(1, page_limit), self.max_limit)
            
            # Calculate pagination
            start_idx = (page - 1) * page_limit
            end_idx = start_idx + page_limit
            
            # Get items for current page
            page_items = items[start_idx:end_idx]
            has_more = end_idx < len(items)
            
            # Create next cursor if there are more items
            next_cursor = None
            if has_more:
                next_cursor_obj = self.create_cursor(
                    page=page + 1,
                    limit=page_limit,
                    filters=filters,
                    sort_order=sort_order
                )
                next_cursor = next_cursor_obj.to_string()
            
            return PaginatedResponse(
                items=page_items,
                nextCursor=next_cursor,
                total_count=len(items),
                has_more=has_more
            )
            
        except Exception as e:
            self.logger.error(f"Pagination failed for {operation}: {e}")
            # Return first page as fallback
            return PaginatedResponse(
                items=items[:self.default_limit],
                nextCursor=None,
                total_count=len(items),
                has_more=len(items) > self.default_limit
            )
    
    def get_pagination_info(self, cursor_string: str) -> Dict[str, Any]:
        """Get information about a pagination cursor."""
        cursor = self.parse_cursor(cursor_string)
        if not cursor:
            return {"error": "Invalid cursor"}
        
        return {
            "page": cursor.page,
            "limit": cursor.limit,
            "filters": cursor.filters,
            "sort_order": cursor.sort_order,
            "timestamp": cursor.timestamp,
            "is_valid": self.validate_cursor(cursor)
        }
