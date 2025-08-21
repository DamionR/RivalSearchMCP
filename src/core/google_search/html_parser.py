#!/usr/bin/env python3
"""
HTML parser for Google Search data extraction.
"""

import re
from typing import List, Union
from bs4 import BeautifulSoup, Tag

from .models import GoogleSearchResult


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
            if result_block.select_one(selector):
                feature_type = selector.split('"')[1].split('_')[-1]
                features.append(f"rich_snippet_{feature_type}")
        
        # Check for featured snippets
        if result_block.find('div', class_='IZ6rdc'):
            features.append("featured_snippet")
        
        # Check for site links
        if result_block.find('div', class_='ULSxyf'):
            features.append("site_links")
        
        # Check for video results
        if result_block.find('div', class_='video-result'):
            features.append("video_result")
        
        # Check for news results
        if result_block.find('div', class_='news-result'):
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
            # Find all search result blocks - try multiple selectors for Google's changing structure
            result_blocks = []
            
            # Try different possible selectors for Google search results
            selectors = [
                "div.g",  # Standard Google result container
                "div[data-hveid]",  # Results with data attributes
                "div.rc",  # Result container
                "div.tF2Cxc",  # Another result container
                "div[jscontroller]",  # Results with JS controllers
            ]
            
            for selector in selectors:
                result_blocks = soup.select(selector)
                if result_blocks:
                    break
            
            # If no results found with selectors, try finding any div with links
            if not result_blocks:
                result_blocks = soup.find_all("div")
                result_blocks = [block for block in result_blocks if isinstance(block, Tag) and block.find("a", href=True)]
            
            for position, result_block in enumerate(result_blocks, 1):
                try:
                    # Ensure result_block is a Tag
                    if not isinstance(result_block, Tag):
                        continue
                        
                    # Extract link - try multiple approaches
                    link_tag = result_block.find("a", href=True)
                    if not link_tag or not isinstance(link_tag, Tag):
                        continue
                    
                    # Extract title - try multiple selectors
                    title = ""
                    title_selectors = [
                        "h3",  # Standard Google title
                        "span.CVA68e",  # Specific class
                        "div[role='heading']",  # ARIA role
                        "a[data-ved]",  # Links with data attributes
                    ]
                    
                    for selector in title_selectors:
                        title_tag = result_block.select_one(selector)
                        if title_tag and isinstance(title_tag, Tag):
                            title = self.clean_text(title_tag.get_text())
                            break
                    
                    # If no title found, try getting text from the link
                    if not title and isinstance(link_tag, Tag):
                        title = self.clean_text(link_tag.get_text())
                    
                    # Extract description - try multiple selectors
                    description = ""
                    desc_selectors = [
                        "span.FrIlee",  # Specific class
                        "div.VwiC3b",  # Description container
                        "span[data-ved]",  # Spans with data attributes
                        "div.s",  # Snippet container
                    ]
                    
                    for selector in desc_selectors:
                        desc_tag = result_block.select_one(selector)
                        if desc_tag and isinstance(desc_tag, Tag):
                            description = self.clean_text(desc_tag.get_text())
                            break
                    
                    # Clean and extract data
                    href = link_tag.get("href", "")
                    if href is None:
                        href = ""
                    link = self._extract_clean_url(str(href))
                    
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
                    print(f"Error parsing individual result: {e}")
                    continue
            
        except Exception as e:
            print(f"Error parsing search results: {e}")
        
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
