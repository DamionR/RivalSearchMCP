"""
Utils package for RivalSearchMCP.
Componentized utility modules for different functionality areas.
"""

# Import all utilities from componentized modules
from .user_agents import (
    get_enhanced_ua_list, get_random_user_agent, get_lynx_user_agent
)
from .http_clients import (
    get_http_client, get_cloudscraper_session, close_http_clients
)
from .html_parsing import (
    create_soup, extract_text_safe, clean_text
)
from .content_processing import (
    clean_html_to_markdown, extract_structured_content,
    format_search_results, format_traversal_results
)
from .error_handling import (
    safe_request, log_operation
)
from .headers_cookies import (
    get_advanced_headers, get_advanced_cookies, get_google_cookies
)

__all__ = [
    # User agent management
    'get_enhanced_ua_list',
    'get_random_user_agent',
    'get_lynx_user_agent',
    # HTTP client management
    'get_http_client',
    'get_cloudscraper_session',
    'close_http_clients',
    # HTML parsing
    'create_soup',
    'extract_text_safe',
    'clean_text',
    # Content processing
    'clean_html_to_markdown',
    'extract_structured_content',
    'format_search_results',
    'format_traversal_results',
    # Error handling
    'safe_request',
    'log_operation',
    # Headers and cookies
    'get_advanced_headers',
    'get_advanced_cookies',
    'get_google_cookies'
]
