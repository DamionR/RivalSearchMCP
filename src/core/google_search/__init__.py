#!/usr/bin/env python3
"""
Google Search Scraper Package

A comprehensive tool for scraping Google Search results with advanced features
like rich snippets detection and traffic estimation.
"""

from .models import GoogleSearchResult
from .scraper import GoogleSearchScraper
from .html_parser import GoogleSearchHTMLParser

__version__ = "1.0.0"
__author__ = "Google Search Scraper"

__all__ = [
    'GoogleSearchResult',
    'GoogleSearchScraper',
    'GoogleSearchHTMLParser'
]
