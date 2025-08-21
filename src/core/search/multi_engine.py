#!/usr/bin/env python3
"""
Multi-engine search component for RivalSearchMCP.
Supports multiple search engines with Google as primary.
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, cast
from urllib.parse import quote_plus
from bs4 import BeautifulSoup, Tag

from src.logger import logger
from src.utils import get_enhanced_ua_list, get_http_client
from .scraper import GoogleSearchScraper

# Additional search engine configurations
ADDITIONAL_ENGINES = {
    "bing": {
        "url": "https://www.bing.com/search",
        "params": {"q": "{query}", "count": "{num}"},
        "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    },
    "duckduckgo": {
        "url": "https://html.duckduckgo.com/html/",
        "params": {"q": "{query}"},
        "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    },
    "yahoo": {
        "url": "https://search.yahoo.com/search",
        "params": {"p": "{query}", "n": "{num}"},
        "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    }
}


class MultiEngineSearch:
    """Multi-engine search with Google as primary and other engines as fallback."""
    
    def __init__(self):
        """Initialize the multi-engine search."""
        self.results = {}
        self.failed_engines = []
        self.user_agents = get_enhanced_ua_list()
    
    async def search_all_engines(
        self, 
        query: str, 
        num_results: int = 10,
        engines: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Search across multiple engines simultaneously.
        
        Args:
            query: Search query
            num_results: Number of results per engine
            engines: List of engines to use (default: all)
            
        Returns:
            Dictionary with results from each engine
        """
        if engines is None:
            engines = ["google"] + list(ADDITIONAL_ENGINES.keys())
        
        logger.info(f"🔍 Multi-engine search for: {query}")
        logger.info(f"🚀 Using engines: {', '.join(engines)}")
        
        # Handle Google search using the dedicated scraper
        if "google" in engines:
            try:
                scraper = GoogleSearchScraper()
                google_results = scraper.search_google(term=query, num_results=num_results)
                # Convert GoogleSearchResult objects to dict format for consistency
                google_dict_results = []
                for result in google_results:
                    google_dict_results.append({
                        'title': result.title,
                        'url': result.url,
                        'snippet': result.description,
                        'position': result.position,
                        'engine': 'google',
                        'domain': result.domain,
                        'search_features': result.search_features
                    })
                self.results["google"] = google_dict_results
                logger.info(f"✅ google: {len(google_dict_results)} results")
            except Exception as e:
                logger.error(f"❌ google search failed: {e}")
                self.failed_engines.append("google")
        
        # Handle other engines
        other_engines = [engine for engine in engines if engine != "google" and engine in ADDITIONAL_ENGINES]
        if other_engines:
            # Create tasks for concurrent search
            tasks = []
            for engine in other_engines:
                task = self._search_engine(engine, query, num_results)
                tasks.append(task)
            
            # Execute all searches concurrently
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                for i, engine in enumerate(other_engines):
                    result = results[i]
                    if isinstance(result, Exception):
                        logger.error(f"❌ {engine} search failed: {result}")
                        self.failed_engines.append(engine)
                    else:
                        self.results[engine] = result
                        logger.info(f"✅ {engine}: {len(result) if isinstance(result, list) else 0} results")
        
        return self._aggregate_results()
    
    async def _search_engine(
        self, 
        engine: str, 
        query: str, 
        num_results: int
    ) -> List[Dict[str, Any]]:
        """Search a single engine (excluding Google)."""
        config = ADDITIONAL_ENGINES[engine]
        
        # Prepare request
        params = config["params"].copy()
        params = {k: v.format(query=quote_plus(query), num=num_results) for k, v in params.items()}
        
        headers = config["headers"].copy()
        headers["User-Agent"] = self._get_random_ua()
        
        try:
            client = await get_http_client()
            response = await client.get(
                config["url"],
                params=params,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            
            # Parse results based on engine
            if engine == "bing":
                return self._parse_bing_results(response.text, num_results)
            elif engine == "duckduckgo":
                return self._parse_duckduckgo_results(response.text, num_results)
            elif engine == "yahoo":
                return self._parse_yahoo_results(response.text, num_results)
            else:
                return self._parse_generic_results(response.text, num_results)
                
        except Exception as e:
            logger.error(f"Error searching {engine}: {e}")
            raise
    
    def _get_random_ua(self) -> str:
        """Get a random user agent."""
        import random
        return random.choice(self.user_agents)
    
    def _parse_bing_results(self, html: str, num_results: int) -> List[Dict[str, Any]]:
        """Parse Bing search results."""
        results = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find search result containers
            result_containers = soup.find_all('li', class_='b_algo')
            
            for i, container in enumerate(result_containers[:num_results]):
                try:
                    # Cast to Tag for proper type checking
                    container_tag = cast(Tag, container)
                    
                    # Extract title and link
                    title_elem = container_tag.find('h2')
                    if title_elem:
                        title_tag = cast(Tag, title_elem)
                        link_elem = title_tag.find('a')
                    else:
                        link_elem = None
                    snippet_elem = container_tag.find('p')
                    
                    if title_elem and link_elem:
                        # Cast elements to Tag for proper type checking
                        title_tag = cast(Tag, title_elem)
                        link_tag = cast(Tag, link_elem)
                        snippet_tag = cast(Tag, snippet_elem) if snippet_elem else None
                        result = {
                            'title': title_tag.get_text(strip=True),
                            'url': link_tag.get('href', ''),
                            'snippet': snippet_tag.get_text(strip=True) if snippet_tag else '',
                            'position': i + 1,
                            'engine': 'bing'
                        }
                        results.append(result)
                except Exception as e:
                    logger.debug(f"Error parsing Bing result: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing Bing results: {e}")
        
        return results
    
    def _parse_duckduckgo_results(self, html: str, num_results: int) -> List[Dict[str, Any]]:
        """Parse DuckDuckGo search results."""
        results = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find search result containers
            result_containers = soup.find_all('div', class_='result')
            
            for i, container in enumerate(result_containers[:num_results]):
                try:
                    # Cast to Tag for proper type checking
                    container_tag = cast(Tag, container)
                    
                    # Extract title and link
                    title_elem = container_tag.find('a', class_='result__a')
                    snippet_elem = container_tag.find('a', class_='result__snippet')
                    
                    if title_elem:
                        # Cast title_elem to Tag for get operation
                        title_tag = cast(Tag, title_elem)
                        result = {
                            'title': title_tag.get_text(strip=True),
                            'url': title_tag.get('href', ''),
                            'snippet': snippet_elem.get_text(strip=True) if snippet_elem else '',
                            'position': i + 1,
                            'engine': 'duckduckgo'
                        }
                        results.append(result)
                except Exception as e:
                    logger.debug(f"Error parsing DuckDuckGo result: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing DuckDuckGo results: {e}")
        
        return results
    
    def _parse_yahoo_results(self, html: str, num_results: int) -> List[Dict[str, Any]]:
        """Parse Yahoo search results."""
        results = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find search result containers
            result_containers = soup.find_all('div', class_='dd')
            
            for i, container in enumerate(result_containers[:num_results]):
                try:
                    # Cast to Tag for proper type checking
                    container_tag = cast(Tag, container)
                    
                    # Extract title and link
                    title_elem = container_tag.find('h3')
                    if title_elem:
                        title_tag = cast(Tag, title_elem)
                        link_elem = title_tag.find('a')
                    else:
                        link_elem = None
                    snippet_elem = container_tag.find('div', class_='compText')
                    
                    if title_elem and link_elem:
                        # Cast elements to Tag for proper type checking
                        title_tag = cast(Tag, title_elem)
                        link_tag = cast(Tag, link_elem)
                        snippet_tag = cast(Tag, snippet_elem) if snippet_elem else None
                        result = {
                            'title': title_tag.get_text(strip=True),
                            'url': link_tag.get('href', ''),
                            'snippet': snippet_tag.get_text(strip=True) if snippet_tag else '',
                            'position': i + 1,
                            'engine': 'yahoo'
                        }
                        results.append(result)
                except Exception as e:
                    logger.debug(f"Error parsing Yahoo result: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing Yahoo results: {e}")
        
        return results
    
    def _parse_generic_results(self, html: str, num_results: int) -> List[Dict[str, Any]]:
        """Parse generic search results."""
        results = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            for i, link in enumerate(links[:num_results]):
                try:
                    # Cast to Tag for proper type checking
                    link_tag = cast(Tag, link)
                    
                    href = link_tag.get('href', '')
                    if isinstance(href, str) and href.startswith('http'):
                        result = {
                            'title': link_tag.get_text(strip=True) or href,
                            'url': href,
                            'snippet': '',
                            'position': i + 1,
                            'engine': 'generic'
                        }
                        results.append(result)
                except Exception as e:
                    logger.debug(f"Error parsing generic result: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing generic results: {e}")
        
        return results
    
    def _aggregate_results(self) -> Dict[str, Any]:
        """Aggregate results from all engines."""
        aggregated = {
            'total_results': sum(len(results) for results in self.results.values()),
            'engines_used': list(self.results.keys()),
            'engines_failed': self.failed_engines,
            'results_by_engine': self.results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Create unified result list
        all_results = []
        for engine, results in self.results.items():
            for result in results:
                result['source_engine'] = engine
                all_results.append(result)
        
        aggregated['all_results'] = all_results
        
        return aggregated
    
    def get_best_results(self, num_results: int = 10) -> List[Dict[str, Any]]:
        """Get the best results across all engines."""
        all_results = []
        for engine, results in self.results.items():
            for result in results:
                result['source_engine'] = engine
                all_results.append(result)
        
        # Sort by position and take top results
        all_results.sort(key=lambda x: x.get('position', 999))
        return all_results[:num_results]
    
    def save_results(self, filename: Optional[str] = None) -> str:
        """Save aggregated results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'debug/multi_engine_search_{timestamp}.json'
        
        aggregated = self._aggregate_results()
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(aggregated, file, indent=2)
        
        logger.info(f"📄 Multi-engine search results saved to {filename}")
        return filename


# Multi-engine convenience function
async def multi_engine_search(
    query: str,
    num_results: int = 10,
    engines: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convenience function for multi-engine search.
    
    Args:
        query: Search query
        num_results: Number of results per engine
        engines: List of engines to use
        
    Returns:
        Aggregated results from all engines
    """
    searcher = MultiEngineSearch()
    return await searcher.search_all_engines(query, num_results, engines)
