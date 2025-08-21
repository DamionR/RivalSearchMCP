#!/usr/bin/env python3
"""
Main entry point for Google Search scraper.
"""

from .scraper import GoogleSearchScraper


def main():
    """Test the Google Search scraper."""
    # Initialize scraper
    scraper = GoogleSearchScraper()
    
    # Search for "ai agents" using Google Search only
    query = "ai agents"
    
    # Use the Google Search only method
    results = scraper.search_google(
        query, 
        num_results=50,  # Back to 50 results
        advanced=True, 
        unique=True
    )
    
    # Display and save results
    scraper.display_results(clean=True)
    scraper.save_results()


if __name__ == "__main__":
    main()
