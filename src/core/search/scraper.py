#!/usr/bin/env python3
"""
Main Google Search scraper class.
"""

import requests
import json
import time
import random
from datetime import datetime
from typing import List, Optional
from bs4 import BeautifulSoup
import cloudscraper

from .models import GoogleSearchResult
from .html_parser import GoogleSearchHTMLParser


class GoogleSearchScraper:
    """Main scraper class for Google Search."""
    
    def __init__(self):
        """Initialize the scraper with session and components."""
        self.scraper = cloudscraper.create_scraper()  # Initialize cloudscraper for Cloudflare bypass
        self.html_parser = GoogleSearchHTMLParser()
        self.results = []
    
    def get_useragent(self) -> str:
        """Generate a random user agent string."""
        lynx_version = f"Lynx/{random.randint(2, 3)}.{random.randint(8, 9)}.{random.randint(0, 2)}"
        libwww_version = f"libwww-FM/{random.randint(2, 3)}.{random.randint(13, 15)}"
        ssl_mm_version = f"SSL-MM/{random.randint(1, 2)}.{random.randint(3, 5)}"
        openssl_version = f"OpenSSL/{random.randint(1, 3)}.{random.randint(0, 4)}.{random.randint(0, 9)}"
        return f"{lynx_version} {libwww_version} {ssl_mm_version} {openssl_version}"
    
    def _make_request(
        self,
        term: str,
        results: int,
        lang: str = "en",
        start: int = 0,
        proxy: Optional[str] = None,
        timeout: int = 5,
        safe: str = "active",
        ssl_verify: Optional[bool] = None,
        region: Optional[str] = None
    ) -> requests.Response:
        """Make a request to Google Search."""
        url = "https://www.google.com/search"
        params = {
            "q": term,
            "num": results + 2,
            "hl": lang,
            "start": start,
            "safe": safe,
            "gl": region,
        }
        
        headers = {
            "User-Agent": self.get_useragent(),
            "Accept": "*/*"
        }
        
        cookies = {
            'CONSENT': 'PENDING+987',
            'SOCS': 'CAESHAgBEhIaAB',
        }
        
        proxies = {"https": proxy, "http": proxy} if proxy else None
        
        response = self.scraper.get(
            url, 
            headers=headers, 
            params=params, 
            proxies=proxies, 
            timeout=timeout, 
            verify=ssl_verify, 
            cookies=cookies
        )
        response.raise_for_status()
        return response
    
    def search_google(
        self,
        term: str,
        num_results: int = 10,
        lang: str = "en",
        proxy: Optional[str] = None,
        advanced: bool = True,
        sleep_interval: float = 0,
        timeout: int = 5,
        safe: str = "active",
        ssl_verify: Optional[bool] = None,
        region: Optional[str] = None,
        start_num: int = 0,
        unique: bool = False
    ) -> List[GoogleSearchResult]:
        """
        Search Google for the given term.
        
        Args:
            term: Search query
            num_results: Number of results to fetch
            lang: Language code
            proxy: Proxy to use
            advanced: Whether to return advanced results with metadata
            sleep_interval: Sleep interval between requests
            timeout: Request timeout
            safe: Safe search setting
            ssl_verify: SSL verification setting
            region: Region code
            start_num: Starting result number
            unique: Whether to ensure unique results
            
        Returns:
            List of GoogleSearchResult objects
        """
        start = start_num
        fetched_results = 0
        fetched_links = set()
        
        print(f"🔍 Searching Google for: {term}")
        print(f"📊 Target results: {num_results}")
        print(f"🌐 Staying within Google Search results only")
        
        while fetched_results < num_results:
            try:
                response = self._make_request(
                    term, 
                    num_results - start, 
                    lang, 
                    start, 
                    proxy, 
                    timeout, 
                    safe, 
                    ssl_verify, 
                    region
                )
                
                soup = BeautifulSoup(response.text, "html.parser")
                new_results = 0
                
                # Parse search results
                search_results = self.html_parser.parse_search_results(soup)
                
                for result in search_results:
                    if result.url in fetched_links and unique:
                        continue
                    
                    fetched_links.add(result.url)
                    fetched_results += 1
                    new_results += 1
                    
                    if advanced:
                        self.results.append(result)
                        print(f"📄 Found result #{fetched_results}: {result.domain}")
                    else:
                        self.results.append(result.url)
                    
                    if fetched_results >= num_results:
                        break
                
                if new_results == 0:
                    break
                    
                start += 10
                time.sleep(sleep_interval)
                
            except Exception as e:
                print(f"Error during search: {e}")
                break
        
        return self.results
    
    def save_results(self) -> str:
        """Save search results to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'debug/google_search_results_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as file:
            if self.results and isinstance(self.results[0], GoogleSearchResult):
                json.dump([result.to_dict() for result in self.results], file, indent=2)
            else:
                json.dump([str(result) for result in self.results], file, indent=2)
        
        print(f"📄 Google search results saved to {filename}")
        return filename
    
    def display_results(self, clean: bool = False):
        """Display search results in a formatted manner."""
        print(f"\n📋 Google Search Results Summary:")
        print(f"Total results: {len(self.results)}")
        
        if self.results:
            for i, result in enumerate(self.results, 1):
                if isinstance(result, GoogleSearchResult):
                    print(f"\n{i}. {result.title}")
                    print(f"   URL: {result.url}")
                    print(f"   Domain: {result.domain}")
                    print(f"   Position: #{result.position}")
                    print(f"   Traffic: {result.estimated_traffic}")
                    if result.search_features:
                        print(f"   Features: {', '.join(result.search_features)}")
                    if result.has_rich_snippet:
                        print(f"   Rich Snippet: {result.rich_snippet_type}")
                else:
                    print(f"{i}. {result}")
        else:
            print("No data found.")
    
    def clear_results(self):
        """Clear stored results."""
        self.results = []
