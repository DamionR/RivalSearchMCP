#!/usr/bin/env python3
"""
HTML parser for Google Search data extraction.
"""

import re
from typing import List, cast
from bs4 import BeautifulSoup, Tag

from .models import GoogleSearchResult
from src.logger import logger


class GoogleSearchHTMLParser:
    """Parser for extracting search results from Google Search HTML."""
    
    def __init__(self):
        """Initialize the parser."""
        pass
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        cleaned_text = re.sub(r'\s+', ' ', text)
        return cleaned_text.strip()
    
    def extract_search_features(self, result_block) -> List[str]:
        """Extract additional features from Google search results."""
        features = []
        
        # Cast to Tag for proper type checking
        result_block_tag = cast(Tag, result_block)
        
        # Check for rich snippets
        rich_snippet_selectors = [
            'div[data-attrid*="rich_snippet"]',
            'div[data-attrid*="knowledge"]',
            'div[data-attrid*="faq"]',
            'div[data-attrid*="review"]',
            'div[data-attrid*="video"]',
            'div[data-attrid*="image"]'
        ]
        
        for selector in rich_snippet_selectors:
            if result_block_tag.select_one(selector):
                feature_type = selector.split('"')[1].split('_')[-1]
                features.append(f"rich_snippet_{feature_type}")
        
        # Check for featured snippets
        if result_block_tag.find('div', class_='IZ6rdc'):
            features.append("featured_snippet")
        
        # Check for site links
        if result_block_tag.find('div', class_='ULSxyf'):
            features.append("site_links")
        
        # Check for video results
        if result_block_tag.find('div', class_='video-result'):
            features.append("video_result")
        
        # Check for news results
        if result_block_tag.find('div', class_='news-result'):
            features.append("news_result")
        
        return features
    
    def estimate_traffic(self, position: int) -> str:
        """Estimate traffic based on search position (rough approximation)."""
        if position <= 3:
            return "high"
        elif position <= 10:
            return "medium"
        else:
            return "low"
    
    def parse_search_results(self, soup: BeautifulSoup) -> List[GoogleSearchResult]:
        """Parse Google Search results from BeautifulSoup object."""
        results = []
        
        try:
            # Find all search result blocks
            result_blocks = soup.find_all("div", class_="ezO2md")
            
            for position, result_block in enumerate(result_blocks, 1):
                try:
                    # Cast to Tag for proper type checking
                    result_block_tag = cast(Tag, result_block)
                    
                    # Extract link
                    link_tag = result_block_tag.find("a", href=True)
                    if not link_tag:
                        continue
                    
                    # Cast link_tag to Tag
                    link_tag = cast(Tag, link_tag)
                    
                    # Extract title
                    title_tag = link_tag.find("span", class_="CVA68e")
                    if not title_tag:
                        continue
                    
                    # Cast title_tag to Tag
                    title_tag = cast(Tag, title_tag)
                    
                    # Extract description
                    description_tag = result_block_tag.find("span", class_="FrIlee")
                    if not description_tag:
                        continue
                    
                    # Cast description_tag to Tag
                    description_tag = cast(Tag, description_tag)
                    
                    # Clean and extract data
                    href = link_tag.get('href', '')
                    if not isinstance(href, str):
                        continue
                    link = self._extract_clean_url(href)
                    title = self.clean_text(title_tag.get_text())
                    description = self.clean_text(description_tag.get_text())
                    
                    if not link or not title:
                        continue
                    
                    # Create search result
                    search_result = GoogleSearchResult(
                        url=link,
                        title=title,
                        description=description,
                        position=position
                    )
                    
                    # Extract additional features
                    search_result.search_features = self.extract_search_features(result_block)
                    search_result.estimated_traffic = self.estimate_traffic(position)
                    
                    # Check for rich snippets
                    if search_result.search_features:
                        search_result.has_rich_snippet = True
                        rich_types = [f for f in search_result.search_features if f.startswith('rich_snippet_')]
                        if rich_types:
                            search_result.rich_snippet_type = rich_types[0].replace('rich_snippet_', '')
                    
                    results.append(search_result)
                    
                except Exception as e:
                    logger.debug(f"Error parsing individual result: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error parsing search results: {e}")
        
        return results
    
    def _extract_clean_url(self, href: str) -> str:
        """Extract clean URL from Google's href attribute."""
        try:
            from urllib.parse import unquote
            # Remove Google's redirect and extract actual URL
            if href.startswith('/url?q='):
                url = href.split('&')[0].replace('/url?q=', '')
                return unquote(url)
            elif href.startswith('http'):
                return href
            else:
                return ""
        except Exception:
            return ""
