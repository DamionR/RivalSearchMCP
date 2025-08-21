#!/usr/bin/env python3
"""
Search result extraction functionality for RivalSearchMCP.
Handles extraction of search results from HTML content.
"""

from typing import List, Dict, cast
from bs4 import BeautifulSoup, Tag


def extract_search_results(html: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Extract search results from HTML content.
    
    Args:
        html: HTML content to extract results from
        max_results: Maximum number of results to extract
        
    Returns:
        List of dictionaries with title, link, and snippet
    """
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    seen_urls = set()
    
    selector_sets = [
        {'container': '#search div[data-hveid]', 'title': 'h3', 'snippet': '.VwiC3b'},
        {'container': '#rso div[data-hveid]', 'title': 'h3', 'snippet': '[data-sncf="1"]'},
        {'container': '.g', 'title': 'h3', 'snippet': 'div[style*="webkit-line-clamp"]'},
        {'container': 'div[jscontroller][data-hveid]', 'title': 'h3', 'snippet': 'div[role="text"]'}
    ]
    alt_snippet_selectors = ['.VwiC3b', '[data-sncf="1"]', 'div[style*="webkit-line-clamp"]', 'div[role="text"]']

    for selectors in selector_sets:
        if len(results) >= max_results:
            break
        containers = soup.select(selectors['container'])
        for container in containers:
            if len(results) >= max_results:
                break
                
            # Cast to Tag for proper type checking
            container_tag = cast(Tag, container)
            
            title_elem = container_tag.select_one(selectors['title'])
            if not title_elem:
                continue
            title = title_elem.text.strip()
            link = ''
            
            link_in_title = title_elem.find_parent('a')
            if link_in_title and hasattr(link_in_title, 'get'):
                link_tag = cast(Tag, link_in_title)
                link = link_tag.get('href', '')
            else:
                parent = title_elem.parent
                while parent and parent.name != 'a':
                    parent = parent.parent
                if parent and parent.name == 'a' and hasattr(parent, 'get'):
                    parent_tag = cast(Tag, parent)
                    link = parent_tag.get('href', '')
                else:
                    container_link = container_tag.find('a')
                    if container_link and hasattr(container_link, 'get'):
                        link_tag = cast(Tag, container_link)
                        link = link_tag.get('href', '')
                    else:
                        link = ''
                        
            if not link or not isinstance(link, str) or not link.startswith('http') or link in seen_urls:
                continue
                
            snippet = ''
            snippet_elem = container_tag.select_one(selectors['snippet'])
            if snippet_elem:
                snippet = snippet_elem.text.strip()
            else:
                for alt in alt_snippet_selectors:
                    elem = container_tag.select_one(alt)
                    if elem:
                        snippet = elem.text.strip()
                        break
                if not snippet:
                    text_divs = []
                    for div in container_tag.find_all('div'):
                        div_tag = cast(Tag, div)
                        if not div_tag.find('h3') and len(div_tag.text.strip()) > 20:
                            text_divs.append(div_tag)
                    if text_divs:
                        snippet = text_divs[0].text.strip()
                        
            if title and link:
                results.append({'title': title, 'link': link, 'snippet': snippet})
                seen_urls.add(link)

    if len(results) < max_results:
        anchors = soup.select("a[href^='http']")
        for a in anchors:
            if len(results) >= max_results:
                break
                
            # Cast to Tag for proper type checking
            anchor_tag = cast(Tag, a)
            
            link = anchor_tag.get('href', '') if hasattr(anchor_tag, 'get') else ''
            if not link or not isinstance(link, str) or not link.startswith('http') or 'google.com' in link or link in seen_urls:
                continue
            title = anchor_tag.text.strip()
            if not title:
                continue
            snippet = ''
            parent = anchor_tag.parent
            for _ in range(3):
                if parent:
                    text = parent.text.strip()
                    if len(text) > 20 and text != title:
                        snippet = text
                        break
                    parent = parent.parent
            results.append({'title': title, 'link': link, 'snippet': snippet})
            seen_urls.add(link)

    return results[:max_results]
