#!/usr/bin/env python3
"""
Multi-engine search implementation for Rival Search MCP.
Replaces Google Search with DuckDuckGo and multiple fallback engines.
"""

import asyncio
import httpx
import json
import re
from typing import List, Dict, Optional, Any
from urllib.parse import quote_plus, urlencode
import time
import random
from dataclasses import dataclass

from src.logger import logger
from src.core.bypass import get_enhanced_ua_list, select_proxy


@dataclass
class SearchResult:
    """Standardized search result format."""
    title: str
    url: str
    snippet: str
    source_engine: str
    rank: int


class MultiSearchEngine:
    """Multi-engine search with fallback capabilities."""
    
    def __init__(self):
        self.user_agents = get_enhanced_ua_list()
        self.session = None
        self.engines = {
            'duckduckgo': {
                'name': 'DuckDuckGo',
                'url': 'https://html.duckduckgo.com/html/',
                'method': self._search_duckduckgo,
                'priority': 1
            },
            'startpage': {
                'name': 'Startpage',
                'url': 'https://www.startpage.com/sp/search',
                'method': self._search_startpage,
                'priority': 2
            },
            'brave': {
                'name': 'Brave Search',
                'url': 'https://search.brave.com/search',
                'method': self._search_brave,
                'priority': 3
            },
            'searx': {
                'name': 'Searx',
                'url': 'https://searx.be/search',
                'method': self._search_searx,
                'priority': 4
            }
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={'User-Agent': random.choice(self.user_agents)}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()
    
    async def search(self, query: str, max_results: int = 10, 
                    engines: Optional[List[str]] = None) -> List[SearchResult]:
        """
        Search across multiple engines with fallback.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            engines: List of engine names to use (default: all)
        
        Returns:
            List of SearchResult objects
        """
        if engines is None:
            engines = ['duckduckgo', 'startpage', 'brave', 'searx']
        
        # Sort engines by priority
        sorted_engines = sorted(
            [(k, v) for k, v in self.engines.items() if k in engines],
            key=lambda x: x[1]['priority']
        )
        
        all_results = []
        
        for engine_key, engine_info in sorted_engines:
            try:
                logger.info(f"Searching with {engine_info['name']}...")
                results = await engine_info['method'](query, max_results)
                
                if results:
                    all_results.extend(results)
                    logger.info(f"✅ {engine_info['name']}: {len(results)} results")
                    
                    # If we have enough results, stop
                    if len(all_results) >= max_results:
                        break
                else:
                    logger.warning(f"⚠️ {engine_info['name']}: No results")
                    
            except Exception as e:
                logger.error(f"❌ {engine_info['name']} failed: {str(e)}")
                continue
        
        # Remove duplicates and limit results
        unique_results = self._deduplicate_results(all_results)
        return unique_results[:max_results]
    
    def _deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Remove duplicate results based on URL."""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            # Normalize URL for comparison
            normalized_url = self._normalize_url(result.url)
            if normalized_url not in seen_urls:
                seen_urls.add(normalized_url)
                unique_results.append(result)
        
        return unique_results
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication."""
        # Remove common tracking parameters
        url = re.sub(r'[?&](utm_|fbclid|gclid|msclkid)=[^&]*', '', url)
        # Remove trailing slash
        url = url.rstrip('/')
        return url.lower()
    
    def _extract_links_regex(self, html_content: str, engine_name: str, max_results: int) -> List[SearchResult]:
        """Extract search results using regex patterns."""
        results = []
        
        # Regex patterns for different search engines
        patterns = {
            'DuckDuckGo': [
                r'<a[^>]*class="[^"]*result__a[^"]*"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>',
                r'<a[^>]*href="([^"]*)"[^>]*class="[^"]*result__title[^"]*"[^>]*>([^<]*)</a>'
            ],
            'Startpage': [
                r'<a[^>]*class="[^"]*result__title[^"]*"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>',
                r'<a[^>]*href="([^"]*)"[^>]*class="[^"]*w-gl__result-title[^"]*"[^>]*>([^<]*)</a>'
            ],
            'Brave Search': [
                r'<a[^>]*class="[^"]*result__title[^"]*"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>',
                r'<a[^>]*href="([^"]*)"[^>]*class="[^"]*web-result__title[^"]*"[^>]*>([^<]*)</a>'
            ]
        }
        
        engine_patterns = patterns.get(engine_name, [r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'])
        
        for pattern in engine_patterns:
            try:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for i, (url, title) in enumerate(matches[:max_results]):
                    if url and title:
                        # Clean up the title and URL
                        title = re.sub(r'<[^>]*>', '', title).strip()
                        url = url.strip()
                        
                        if title and url and not url.startswith('#'):
                            results.append(SearchResult(
                                title=title,
                                url=url,
                                snippet="",  # We'll add snippet extraction later if needed
                                source_engine=engine_name,
                                rank=len(results) + 1
                            ))
                            
                            if len(results) >= max_results:
                                break
                
                if results:
                    break  # Found results with this pattern
                    
            except Exception as e:
                logger.debug(f"Error with pattern {pattern}: {e}")
                continue
        
        return results
    
    async def _search_duckduckgo(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using DuckDuckGo HTML interface."""
        try:
            params = {
                'q': query,
                'kl': 'us-en',  # Language/region
                'kp': '1',      # Safe search off
                't': 'h_'       # HTML interface
            }
            
            if self.session is None:
                raise RuntimeError("Session not initialized")
            response = await self.session.get(
                self.engines['duckduckgo']['url'],
                params=params
            )
            response.raise_for_status()
            
            return self._extract_links_regex(response.text, 'DuckDuckGo', max_results)
            
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []
    
    async def _search_startpage(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Startpage (Google results without tracking)."""
        try:
            params = {
                'query': query,
                'cat': 'web',
                'language': 'english',
                'engines': 'google'
            }
            
            if self.session is None:
                raise RuntimeError("Session not initialized")
            response = await self.session.get(
                self.engines['startpage']['url'],
                params=params
            )
            response.raise_for_status()
            
            return self._extract_links_regex(response.text, 'Startpage', max_results)
            
        except Exception as e:
            logger.error(f"Startpage search failed: {e}")
            return []
    
    async def _search_brave(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Brave Search."""
        try:
            params = {
                'q': query,
                'source': 'web'
            }
            
            if self.session is None:
                raise RuntimeError("Session not initialized")
            response = await self.session.get(
                self.engines['brave']['url'],
                params=params
            )
            response.raise_for_status()
            
            return self._extract_links_regex(response.text, 'Brave Search', max_results)
            
        except Exception as e:
            logger.error(f"Brave search failed: {e}")
            return []
    
    async def _search_searx(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Searx meta-search engine."""
        try:
            params = {
                'q': query,
                'engines': 'google,duckduckgo,startpage',
                'format': 'json',
                'results': max_results
            }
            
            if self.session is None:
                raise RuntimeError("Session not initialized")
            response = await self.session.get(
                self.engines['searx']['url'],
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'results' in data and isinstance(data['results'], list):
                for i, result in enumerate(data['results'][:max_results]):
                    try:
                        if isinstance(result, dict):
                            title = result.get('title', '') if result.get('title') is not None else ''
                            url = result.get('url', '') if result.get('url') is not None else ''
                            snippet = result.get('content', '') if result.get('content') is not None else ''
                            
                            results.append(SearchResult(
                                title=title,
                                url=url,
                                snippet=snippet,
                                source_engine='Searx',
                                rank=i + 1
                            ))
                    except Exception as e:
                        logger.debug(f"Error parsing Searx result: {e}")
                        continue
            
            return results
            
        except Exception as e:
            logger.error(f"Searx search failed: {e}")
            return []


# Convenience functions for backward compatibility
async def multi_search(query: str, max_results: int = 10, 
                      engines: Optional[List[str]] = None) -> List[SearchResult]:
    """Convenience function for multi-engine search."""
    async with MultiSearchEngine() as searcher:
        return await searcher.search(query, max_results, engines)


async def duckduckgo_search(query: str, max_results: int = 10) -> List[SearchResult]:
    """Search using DuckDuckGo only."""
    return await multi_search(query, max_results, ['duckduckgo'])


async def startpage_search(query: str, max_results: int = 10) -> List[SearchResult]:
    """Search using Startpage only."""
    return await multi_search(query, max_results, ['startpage'])
