"""
Utility functions for RivalSearchMCP.
Helper functions and utilities for various components.
"""

# Import utility functions from submodules
from .content import clean_html_to_markdown, format_traversal_results
from .error import log_operation, safe_request
from .headers import (
    get_advanced_cookies,
    get_advanced_headers,
    get_google_cookies,
)
from .parsing import clean_text, create_soup, extract_text_safe
from .clients import close_http_clients, get_cloudscraper_session, get_http_client
from .llms import (
    categorize_page_advanced,
    clean_html_content,
    cleanup_temp_files,
    create_output_directory,
    extract_domain,
    extract_page_metadata,
    extract_text_from_html,
    format_llms_txt_metadata,
    generate_summary,
    normalize_url,
    sanitize_filename,
    validate_llms_txt_content,
    validate_url,
)

# Import new utility modules
from .trends import (
    calculate_trend_statistics,
    cleanup_export_files,
    create_export_directory,
    create_trends_database,
    export_to_excel,
    format_date_range,
    generate_filename,
    sanitize_table_name,
    validate_region,
    validate_resolution,
    validate_timeframe,
)
from .agents import (
    get_enhanced_ua_list,
    get_lynx_user_agent,
    get_random_user_agent,
)

__all__ = [
    # Content processing utilities
    "clean_html_to_markdown",
    "format_traversal_results",
    # User agent management
    "get_enhanced_ua_list",
    "get_random_user_agent",
    "get_lynx_user_agent",
    # HTTP client management
    "get_http_client",
    "get_cloudscraper_session",
    "close_http_clients",
    # HTML parsing
    "create_soup",
    "extract_text_safe",
    "clean_text",
    # Error handling
    "safe_request",
    "log_operation",
    # Headers and cookies
    "get_advanced_headers",
    "get_advanced_cookies",
    "get_google_cookies",
    # Google Trends utilities
    "generate_filename",
    "create_export_directory",
    "sanitize_table_name",
    "format_date_range",
    "validate_timeframe",
    "validate_region",
    "validate_resolution",
    "calculate_trend_statistics",
    "export_to_excel",
    "create_trends_database",
    "cleanup_export_files",
    # LLMs.txt Generator utilities
    "normalize_url",
    "validate_url",
    "create_output_directory",
    "sanitize_filename",
    "extract_domain",
    "categorize_page_advanced",
    "extract_page_metadata",
    "clean_html_content",
    "extract_text_from_html",
    "generate_summary",
    "validate_llms_txt_content",
    "format_llms_txt_metadata",
    "cleanup_temp_files",
]
