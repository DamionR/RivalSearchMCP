"""
Yahoo search engine implementation for RivalSearchMCP.
Uses HTML format for most reliable results.
"""

from typing import List
from bs4 import BeautifulSoup, Tag
from datetime import datetime

from ...core.multi_engines import BaseSearchEngine, MultiSearchResult
from src.logging.logger import logger


class YahooSearchEngine(BaseSearchEngine):
    """Yahoo search engine implementation - HTML format only."""
    
    def __init__(self):
        super().__init__("Yahoo", "https://search.yahoo.com")
    
    async def search(
        self, 
        query: str, 
        num_results: int = 10,
        extract_content: bool = True,
        follow_links: bool = True,
        max_depth: int = 2
    ) -> List[MultiSearchResult]:
        """Search Yahoo using HTML format (most reliable)."""
        try:
            logger.info(f"Starting Yahoo search for: {query}")
            
            # Use only HTML format (most reliable)
            results = await self._search_html(query, num_results)
            
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
            
            logger.info(f"Yahoo search completed: {len(results)} results with content extraction")
            return results
            
        except Exception as e:
            logger.error(f"Yahoo search failed: {e}")
            return []
    
    async def _search_html(self, query: str, num_results: int) -> List[MultiSearchResult]:
        """Search using HTML format (most reliable)."""
        search_url = f"{self.base_url}/search"
        params = {
            'p': query,
            'n': min(num_results, 50),
            'ei': 'UTF-8',
            'fr': 'yfp-t'
        }
        
        try:
            async with self.session as client:
                response = await client.get(search_url, params=params)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                
                # Find result containers
                result_containers = soup.find_all('div', class_='dd')
                if not result_containers:
                    # Try alternative selectors
                    result_containers = soup.find_all('div', class_='algo')
                
                for i, container in enumerate(result_containers[:num_results]):
                    try:
                        if isinstance(container, Tag):
                            # Extract title and link
                            title_elem = container.find('a')
                            
                            if isinstance(title_elem, Tag) and hasattr(title_elem, 'get_text') and callable(getattr(title_elem, 'get_text')):
                                title = self._clean_text(title_elem.get_text())
                                url = title_elem.get('href', '')
                                
                                # Extract description
                                desc_elem = container.find('div', class_='compText')
                                if not desc_elem:
                                    desc_elem = container.find('span', class_='st')
                                
                                description = ""
                                if isinstance(desc_elem, Tag) and hasattr(desc_elem, 'get_text') and callable(getattr(desc_elem, 'get_text')):
                                    description = self._clean_text(desc_elem.get_text())
                                
                                if title and url:
                                    results.append(MultiSearchResult(
                                        title=title,
                                        url=str(url),
                                        description=description,
                                        engine=self.name,
                                        position=i + 1,
                                        timestamp=datetime.now().isoformat(),
                                        html_structure=self._extract_html_structure(str(container)),
                                        raw_html=str(container)
                                    ))
                    except Exception as e:
                        logger.debug(f"Failed to parse result {i}: {e}")
                        continue
                
                return results
                
        except Exception as e:
            logger.error(f"Yahoo HTML search failed: {e}")
            return []
