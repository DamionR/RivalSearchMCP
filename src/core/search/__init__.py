#!/usr/bin/env python3
"""
Google Search Scraper Package

A comprehensive tool for scraping Google Search results with advanced features
like rich snippets detection and traffic estimation.
"""

from .models import GoogleSearchResult
from .scraper import GoogleSearchScraper
from .html_parser import GoogleSearchHTMLParser
from .multi_engine import MultiEngineSearch, multi_engine_search
from .ocr_processing import process_images_ocr

__version__ = "1.0.0"
__author__ = "Google Search Scraper"

__all__ = [
    'GoogleSearchResult',
    'GoogleSearchScraper',
    'GoogleSearchHTMLParser',
    'MultiEngineSearch',
    'multi_engine_search',
    'process_images_ocr'
]
