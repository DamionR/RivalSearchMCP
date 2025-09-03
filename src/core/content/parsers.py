#!/usr/bin/env python3
"""
Unified HTML parsers for RivalSearchMCP.
Consolidates the best parsing methods from all modules.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, Tag

from src.logging.logger import logger


class BaseHTMLParser(ABC):
    """Base class for HTML parsers."""
    
    def __init__(self):
        """Initialize the parser."""
        pass
    
    @abstractmethod
    def parse(self, html_content: str, **kwargs) -> Any:
        """Parse HTML content using the parser's method."""
        pass


class UnifiedHTMLParser(BaseHTMLParser):
    """Unified HTML parser with multiple parsing strategies."""
    
    def parse(self, html_content: str, **kwargs) -> Dict[str, Any]:
        """Parse HTML structure and extract comprehensive information."""
        if not html_content:
            return {}
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            structure = {
                "title": "",
                "meta_description": "",
                "headings": [],
                "links": [],
                "images": [],
                "forms": [],
                "tables": [],
                "main_content": "",
                "metadata": {}
            }
            
            # Extract title
            title_tag = soup.find("title")
            if isinstance(title_tag, Tag) and hasattr(title_tag, 'get_text'):
                structure["title"] = title_tag.get_text().strip()
            
            # Extract meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if isinstance(meta_desc, Tag) and hasattr(meta_desc, 'get'):
                structure["meta_description"] = meta_desc.get("content", "")
            
            # Extract headings
            for i in range(1, 7):
                headings = soup.find_all(f"h{i}")
                for heading in headings:
                    if isinstance(heading, Tag) and hasattr(heading, 'get_text'):
                        structure["headings"].append({
                            "level": i,
                            "text": heading.get_text().strip(),
                            "id": heading.get("id", "")
                        })
            
            # Extract links
            links = soup.find_all("a", href=True)
            for link in links:
                if isinstance(link, Tag) and hasattr(link, 'get'):
                    structure["links"].append({
                        "text": link.get_text().strip(),
                        "href": link.get("href", ""),
                        "title": link.get("title", "")
                    })
            
            # Extract images
            images = soup.find_all("img")
            for img in images:
                if isinstance(img, Tag) and hasattr(img, 'get'):
                    structure["images"].append({
                        "alt": img.get("alt", ""),
                        "src": img.get("src", ""),
                        "title": img.get("title", "")
                    })
            
            # Extract forms
            forms = soup.find_all("form")
            for form in forms:
                if isinstance(form, Tag) and hasattr(form, 'get'):
                    inputs = form.find_all("input")
                    structure["forms"].append({
                        "action": form.get("action", ""),
                        "method": form.get("method", ""),
                        "inputs": len(inputs) if inputs else 0
                    })
            
            # Extract tables
            tables = soup.find_all("table")
            for table in tables:
                if isinstance(table, Tag):
                    rows = table.find_all("tr")
                    cell_count = 0
                    for row in rows:
                        if isinstance(row, Tag):
                            cells = row.find_all(["td", "th"])
                            cell_count += len(cells) if cells else 0
                    structure["tables"].append({
                        "rows": len(rows),
                        "cells": cell_count
                    })
            
            # Extract metadata
            structure["metadata"] = self._extract_metadata(soup)
            
            return structure
            
        except Exception as e:
            logger.error(f"HTML structure extraction failed: {e}")
            return {}
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract metadata from HTML content."""
        metadata = {}

        # Extract meta tags
        meta_tags = soup.find_all("meta")
        for meta in meta_tags:
            if isinstance(meta, Tag) and hasattr(meta, 'get'):
                name = meta.get("name", meta.get("property", ""))
                content = meta.get("content", "")
                if name and content:
                    metadata[name] = content

        # Extract Open Graph tags
        og_tags = soup.find_all("meta", property=re.compile(r"^og:"))
        for og in og_tags:
            if isinstance(og, Tag) and hasattr(og, 'get'):
                property_name = og.get("property", "")
                content = og.get("content", "")
                if property_name and content:
                    metadata[property_name] = content

        return metadata


class GoogleSearchParser(BaseHTMLParser):
    """Google search-specific HTML parser."""
    
    def parse(self, html_content: str, **kwargs) -> List[Dict[str, str]]:
        """Parse Google search results HTML."""
        from .extractors import GoogleSpecificExtractor
        
        extractor = GoogleSpecificExtractor()
        return extractor.extract(html_content, **kwargs)


class DocumentationParser(BaseHTMLParser):
    """Documentation website HTML parser."""
    
    def parse(self, html_content: str, **kwargs) -> Dict[str, Any]:
        """Parse documentation HTML for LLMs.txt generation."""
        from .extractors import GenericContentExtractor
        
        extractor = GenericContentExtractor()
        main_content = extractor.extract(html_content, **kwargs)
        
        # Parse structure
        structure_parser = UnifiedHTMLParser()
        structure = structure_parser.parse(html_content, **kwargs)
        
        # Add main content
        structure["main_content"] = main_content
        
        return structure
