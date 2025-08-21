"""
Common schemas for FastMCP server.
Handles generic response schemas and common data structures.
"""

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool = Field(default=True, description="Operation success")
    message: str = Field(description="Success message")
