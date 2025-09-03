"""
Bing search engine implementation for RivalSearchMCP.
Uses RSS format for most reliable results.
"""

from typing import List
from bs4 import BeautifulSoup, Tag
from datetime import datetime

from ...core.multi_engines import BaseSearchEngine, MultiSearchResult
from src.logging.logger import logger


class BingSearchEngine(BaseSearchEngine):
    """Bing search engine implementation - RSS format only (most reliable)."""
    
    def __init__(self):
        super().__init__("Bing", "https://www.bing.com")
    
    async def search(
        self, 
        query: str, 
        num_results: int = 10,
        extract_content: bool = True,
        follow_links: bool = True,
        max_depth: int = 2
    ) -> List[MultiSearchResult]:
        """Search Bing using RSS format (most reliable method)."""
        try:
            logger.info(f"Starting Bing search for: {query}")
            
            # Use only RSS format (most reliable)
            results = await self._search_rss(query, num_results)
            
            if extract_content and results:
                # Extract real URLs and fetch content
                for result in results:
                    result.real_url = self._extract_real_url(result.url)
                    
                    # Always fetch content when content extraction is enabled
                    target_url = result.real_url if result.real_url != result.url else result.url
                    if target_url:
                        logger.info(f"Following link to: {target_url}")
                        content = await self._fetch_page_content(target_url)
                        
                        if content:
                            # Extract main content using the enhanced multi-method approach
                            result.full_content = self._extract_main_content(content)
                            result.internal_links = self._extract_internal_links(content, target_url)
                            result.html_structure = self._extract_html_structure(content)
                            
                            if follow_links and result.internal_links and max_depth > 1:
                                result.second_level_content = await self._extract_second_level_content(
                                    target_url, result.internal_links
                                )
            
            logger.info(f"Bing search completed: {len(results)} results with content extraction")
            return results
            
        except Exception as e:
            logger.error(f"Bing search failed: {e}")
            return []
    
    async def _search_rss(self, query: str, num_results: int) -> List[MultiSearchResult]:
        """Search using RSS format (most reliable)."""
        search_url = f"{self.base_url}/search"
        params = {
            'q': query,
            'count': min(num_results, 50),
            'format': 'rss'
        }
        
        try:
            async with self.session as client:
                response = await client.get(search_url, params=params)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'xml')
                items = soup.find_all('item')
                
                results = []
                for i, item in enumerate(items[:num_results]):
                    if isinstance(item, Tag):
                        title_elem = item.find('title')
                        title = self._clean_text(title_elem.text if isinstance(title_elem, Tag) and hasattr(title_elem, 'text') else '')
                        link_elem = item.find('link')
                        link = link_elem.text if isinstance(link_elem, Tag) and hasattr(link_elem, 'text') else ''
                        desc_elem = item.find('description')
                        description = self._clean_text(desc_elem.text if isinstance(desc_elem, Tag) and hasattr(desc_elem, 'text') else '')
                        
                        if title and link:
                            results.append(MultiSearchResult(
                                title=title,
                                url=link,
                                description=description,
                                engine=self.name,
                                position=i + 1,
                                timestamp=datetime.now().isoformat(),
                                html_structure=self._extract_html_structure(response.text),
                                raw_html=str(item)
                            ))
                
                return results
                
        except Exception as e:
            logger.error(f"Bing RSS search failed: {e}")
            return []
