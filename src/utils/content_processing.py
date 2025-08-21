"""
Content processing utilities for RivalSearchMCP.
Handles HTML cleaning, markdown formatting, and content optimization.
"""

import re
from typing import List, Optional, Union, cast
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString, PageElement
from urllib.parse import urljoin, urlparse


def clean_html_to_markdown(html_content: str, base_url: str = "") -> str:
    """
    Convert HTML content to clean markdown format.
    
    Args:
        html_content: Raw HTML content
        base_url: Base URL for resolving relative links
        
    Returns:
        Clean markdown formatted content
    """
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    _remove_unwanted_elements(soup)
    
    # Convert to markdown
    markdown_content = _convert_to_markdown(soup, base_url)
    
    # Clean and optimize
    return _optimize_content(markdown_content)


def _remove_unwanted_elements(soup: BeautifulSoup) -> None:
    """Remove unwanted HTML elements."""
    # Remove script and style elements
    for element in soup(["script", "style", "noscript", "iframe", "embed", "object"]):
        element.decompose()
    
    # Remove navigation, footer, header elements
    for element in soup(["nav", "footer", "header", "aside", "menu"]):
        element.decompose()
    
    # Remove common ad and tracking elements
    for element in soup.find_all(class_=re.compile(r'(ad|ads|advertisement|banner|tracking|analytics|cookie|popup|modal|overlay)', re.I)):
        element.decompose()
    
    # Remove elements with common ad IDs
    for element in soup.find_all(id=re.compile(r'(ad|ads|banner|tracking|analytics|cookie|popup|modal|overlay)', re.I)):
        element.decompose()


def _convert_to_markdown(soup: BeautifulSoup, base_url: str) -> str:
    """Convert BeautifulSoup object to markdown."""
    content_parts = []
    
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'a', 'strong', 'em', 'code', 'pre', 'blockquote', 'table', 'tr', 'td', 'th']):
        if isinstance(element, Tag):
            content_parts.append(_process_element(cast(Tag, element), base_url))
    
    return '\n'.join(content_parts)


def _process_element(element: Tag, base_url: str) -> str:
    """Process individual HTML elements to markdown."""
    tag_name = element.name
    
    if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level = int(tag_name[1])
        text = element.get_text(strip=True)
        return f"{'#' * level} {text}"
    
    elif tag_name == 'p':
        text = _process_inline_elements(element, base_url)
        return text if text.strip() else ""
    
    elif tag_name in ['ul', 'ol']:
        items = []
        for li in element.find_all('li', recursive=False):
            if isinstance(li, Tag):
                item_text = _process_inline_elements(cast(Tag, li), base_url)
                if item_text.strip():
                    marker = "- " if tag_name == 'ul' else "1. "
                    items.append(f"{marker}{item_text}")
        return '\n'.join(items)
    
    elif tag_name == 'li':
        text = _process_inline_elements(element, base_url)
        return f"- {text}" if text.strip() else ""
    
    elif tag_name == 'a':
        text = element.get_text(strip=True)
        href = element.get('href', '')
        if href and text:
            href_str = str(href)
            if base_url and not href_str.startswith(('http://', 'https://')):
                href_str = urljoin(base_url, href_str)
            return f"[{text}]({href_str})"
        return text
    
    elif tag_name == 'strong':
        text = element.get_text(strip=True)
        return f"**{text}**" if text else ""
    
    elif tag_name == 'em':
        text = element.get_text(strip=True)
        return f"*{text}*" if text else ""
    
    elif tag_name == 'code':
        text = element.get_text(strip=True)
        return f"`{text}`" if text else ""
    
    elif tag_name == 'pre':
        text = element.get_text(strip=True)
        return f"```\n{text}\n```" if text else ""
    
    elif tag_name == 'blockquote':
        text = element.get_text(strip=True)
        lines = text.split('\n')
        return '\n'.join(f"> {line}" for line in lines if line.strip())
    
    elif tag_name in ['table', 'tr', 'td', 'th']:
        return _process_table_element(element)
    
    return element.get_text(strip=True)


def _process_inline_elements(element: Tag, base_url: str) -> str:
    """Process inline elements within a block element."""
    text_parts = []
    
    for child in element.children:
        if isinstance(child, NavigableString):
            text = child.strip()
            if text:
                text_parts.append(text)
        elif isinstance(child, Tag):
            processed = _process_element(child, base_url)
            if processed:
                text_parts.append(processed)
        # Skip other types like Comment, Doctype, etc.
    
    return ' '.join(text_parts)


def _process_table_element(element: Tag) -> str:
    """Process table elements to markdown."""
    if element.name == 'table':
        rows = element.find_all('tr')
        if not rows:
            return ""
        
        # Process header
        header_row = rows[0]
        if isinstance(header_row, Tag):
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td']) if isinstance(th, Tag)]
            if not headers:
                return ""
            
            # Create markdown table
            table_lines = ['| ' + ' | '.join(headers) + ' |']
            table_lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
            
            # Process data rows
            for row in rows[1:]:
                if isinstance(row, Tag):
                    cells = [td.get_text(strip=True) for td in row.find_all('td') if isinstance(td, Tag)]
                    if cells:
                        table_lines.append('| ' + ' | '.join(cells) + ' |')
        
        return '\n'.join(table_lines)
    
    return ""


def _optimize_content(content: str) -> str:
    """
    Optimize content for single-line delimited format.
    
    Args:
        content: Raw markdown content
        
    Returns:
        Optimized single-line delimited content
    """
    if not content:
        return ""
    
    # Split into lines and clean each line
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Clean the line
        cleaned_line = _clean_line(line)
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    
    # Join with single-line delimiter
    return ' | '.join(cleaned_lines)


def _clean_line(line: str) -> str:
    """Clean a single line of content."""
    if not line or not line.strip():
        return ""
    
    # Remove excessive whitespace
    line = re.sub(r'\s+', ' ', line.strip())
    
    # Remove common unwanted patterns
    line = re.sub(r'^\s*[-*+]\s*$', '', line)  # Empty list items
    line = re.sub(r'^\s*>\s*$', '', line)      # Empty blockquotes
    line = re.sub(r'^\s*#+\s*$', '', line)     # Empty headers
    
    # Clean up markdown formatting
    line = re.sub(r'\*\*\s+\*\*', '', line)    # Empty bold
    line = re.sub(r'\*\s+\*', '', line)        # Empty italic
    line = re.sub(r'`\s+`', '', line)          # Empty code
    
    # Remove excessive punctuation
    line = re.sub(r'[.!?]{3,}', '...', line)
    line = re.sub(r'[-_]{3,}', '---', line)
    
    return line.strip()


def extract_structured_content(html_content: str, base_url: str = "") -> dict:
    """
    Extract structured content from HTML.
    
    Args:
        html_content: Raw HTML content
        base_url: Base URL for resolving relative links
        
    Returns:
        Dictionary with structured content
    """
    if not html_content:
        return {}
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title = ""
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
    
    # Extract meta description
    description = ""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and isinstance(meta_desc, Tag):
        description = meta_desc.get('content', '')
    
    # Extract main content
    main_content = _extract_main_content(soup)
    
    # Convert to markdown
    markdown_content = clean_html_to_markdown(main_content, base_url)
    
    return {
        'title': title,
        'description': description,
        'content': markdown_content,
        'url': base_url
    }


def _extract_main_content(soup: BeautifulSoup) -> str:
    """Extract main content from HTML."""
    # Try to find main content areas
    main_selectors = [
        'main',
        '[role="main"]',
        '.main-content',
        '.content',
        '.post-content',
        '.article-content',
        '#content',
        '#main'
    ]
    
    for selector in main_selectors:
        main_element = soup.select_one(selector)
        if main_element:
            return str(main_element)
    
    # Fallback: remove navigation and get body content
    _remove_unwanted_elements(soup)
    body = soup.find('body')
    if body:
        return str(body)
    
    return str(soup)


def format_search_results(results: List[dict]) -> str:
    """
    Format search results as clean markdown.
    
    Args:
        results: List of search result dictionaries
        
    Returns:
        Formatted search results
    """
    if not results:
        return "No search results found."
    
    formatted_parts = []
    
    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        url = result.get('url', '')
        snippet = result.get('snippet', '')
        
        # Format as numbered list with markdown
        formatted_parts.append(f"{i}. **{title}**")
        if url:
            formatted_parts.append(f"   URL: {url}")
        if snippet:
            formatted_parts.append(f"   Snippet: {snippet}")
        formatted_parts.append("")  # Empty line between results
    
    return ' | '.join(formatted_parts)


def format_traversal_results(pages: List[dict]) -> str:
    """
    Format website traversal results as clean markdown.
    
    Args:
        pages: List of page dictionaries
        
    Returns:
        Formatted traversal results
    """
    if not pages:
        return "No pages found."
    
    formatted_parts = []
    
    for i, page in enumerate(pages, 1):
        url = page.get('url', '')
        title = page.get('title', 'No title')
        content = page.get('content', '')
        depth = page.get('depth', 0)
        
        # Format with depth indicator
        indent = "  " * depth
        formatted_parts.append(f"{i}. {indent}**{title}** (depth {depth})")
        if url:
            formatted_parts.append(f"{indent}   URL: {url}")
        if content:
            # Truncate content for summary
            content_preview = content[:200] + "..." if len(content) > 200 else content
            formatted_parts.append(f"{indent}   Content: {content_preview}")
    
    return ' | '.join(formatted_parts)
