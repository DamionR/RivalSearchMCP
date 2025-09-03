"""
LLMs.txt Generator core functionality for RivalSearchMCP.
Handles website documentation generation following the llmstxt.org specification.
"""

from .generator import ContentProcessor, LLMsTxtGenerator

__all__ = ["LLMsTxtGenerator", "ContentProcessor"]
