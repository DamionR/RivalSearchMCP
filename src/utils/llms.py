"""
LLMs.txt Generator utility functions for RivalSearchMCP.
Helper functions for documentation generation and processing.
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from src.logging.logger import logger


def normalize_url(url: str) -> str:
    """
    Normalize URL for consistent processing.

    Args:
        url: Raw URL string

    Returns:
        Normalized URL
    """
    # Remove @ prefix if present
    if url.startswith("@"):
        url = url[1:]

    # Add protocol if missing
    if not url.startswith(("http://", "https://", "file://")):
        if os.path.exists(url):
            url = f"file://{os.path.abspath(url)}"
        else:
            url = f"https://{url}"

    return url


def validate_url(url: str) -> bool:
    """
    Validate URL format and accessibility.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False


def create_output_directory(output_dir: str) -> Path:
    """
    Create output directory for generated files.

    Args:
        output_dir: Output directory path

    Returns:
        Path to created directory
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 Created output directory: {output_path}")
    return output_path


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file creation.

    Args:
        filename: Raw filename

    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(" .")

    # Ensure it's not empty
    if not sanitized:
        sanitized = "untitled"

    return sanitized


def extract_domain(url: str) -> str:
    """
    Extract domain from URL.

    Args:
        url: URL string

    Returns:
        Domain name
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return "unknown"


def categorize_page_advanced(
    title: str,
    content: str,
    url: str,
    custom_rules: Optional[Dict[str, List[str]]] = None,
) -> str:
    """
    Advanced page categorization with custom rules.

    Args:
        title: Page title
        content: Page content
        url: Page URL
        custom_rules: Custom categorization rules

    Returns:
        Page category
    """
    title_lower = title.lower()
    content_lower = content.lower()
    url_lower = url.lower()

    # Default categorization rules
    default_rules = {
        "API Reference": [
            "api",
            "reference",
            "docs",
            "documentation",
            "endpoint",
            "method",
        ],
        "Guides & Tutorials": [
            "guide",
            "tutorial",
            "how-to",
            "getting started",
            "learn",
            "walkthrough",
        ],
        "Examples & Demos": [
            "example",
            "sample",
            "demo",
            "code sample",
            "implementation",
        ],
        "Installation & Setup": [
            "install",
            "setup",
            "configuration",
            "getting started",
            "prerequisites",
        ],
        "Help & Support": [
            "faq",
            "help",
            "support",
            "troubleshooting",
            "common issues",
            "error",
        ],
        "Blog & News": [
            "blog",
            "news",
            "announcement",
            "release",
            "update",
            "changelog",
        ],
        "Contributing": [
            "contributing",
            "contribute",
            "development",
            "pull request",
            "issue",
        ],
        "Community": ["community", "forum", "discussion", "chat", "discord", "slack"],
    }

    # Use custom rules if provided
    rules = custom_rules if custom_rules else default_rules

    # Score each category
    category_scores = {}
    for category, keywords in rules.items():
        score = 0
        for keyword in keywords:
            if keyword in title_lower:
                score += 3  # Title matches are more important
            if keyword in content_lower:
                score += 1
            if keyword in url_lower:
                score += 2  # URL matches are also important

        if score > 0:
            category_scores[category] = score

    # Return highest scoring category
    if category_scores:
        best_category = max(category_scores.items(), key=lambda x: x[1])[0]
        return best_category

    return "Other"


def extract_page_metadata(html_content: str) -> Dict[str, str]:
    """
    Extract metadata from HTML content.

    Args:
        html_content: Raw HTML content

    Returns:
        Dictionary of metadata
    """
    metadata = {}

    # Extract meta tags
    meta_pattern = r'<meta\s+name=["\']([^"\']+)["\']\s+content=["\']([^"\']+)["\']'
    meta_matches = re.findall(meta_pattern, html_content, re.IGNORECASE)

    for name, content in meta_matches:
        metadata[name.lower()] = content

    # Extract Open Graph tags
    og_pattern = (
        r'<meta\s+property=["\']og:([^"\']+)["\']\s+content=["\']([^"\']+)["\']'
    )
    og_matches = re.findall(og_pattern, html_content, re.IGNORECASE)

    for property_name, content in og_matches:
        metadata[f"og:{property_name}"] = content

    # Extract title
    title_pattern = r"<title[^>]*>([^<]+)</title>"
    title_match = re.search(title_pattern, html_content, re.IGNORECASE)
    if title_match:
        metadata["title"] = title_match.group(1).strip()

    return metadata


def clean_html_content(html_content: str) -> str:
    """
    Clean HTML content for better text extraction.

    Args:
        html_content: Raw HTML content

    Returns:
        Cleaned HTML content
    """
    # Remove script and style tags
    html_content = re.sub(
        r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE
    )
    html_content = re.sub(
        r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL | re.IGNORECASE
    )

    # Remove comments
    html_content = re.sub(r"<!--.*?-->", "", html_content, flags=re.DOTALL)

    # Remove common unwanted elements
    unwanted_patterns = [
        r"<nav[^>]*>.*?</nav>",
        r"<footer[^>]*>.*?</footer>",
        r"<header[^>]*>.*?</header>",
        r"<aside[^>]*>.*?</aside>",
        r"<menu[^>]*>.*?</menu>",
        r"<noscript[^>]*>.*?</noscript>",
    ]

    for pattern in unwanted_patterns:
        html_content = re.sub(
            pattern, "", html_content, flags=re.DOTALL | re.IGNORECASE
        )

    return html_content


def extract_text_from_html(html_content: str) -> str:
    """
    Extract clean text from HTML content.

    Args:
        html_content: HTML content

    Returns:
        Clean text content
    """
    # Clean HTML first
    clean_html = clean_html_content(html_content)

    # Remove HTML tags
    text_content = re.sub(r"<[^>]+>", "", clean_html)

    # Decode HTML entities
    text_content = text_content.replace("&amp;", "&")
    text_content = text_content.replace("&lt;", "<")
    text_content = text_content.replace("&gt;", ">")
    text_content = text_content.replace("&quot;", '"')
    text_content = text_content.replace("&#39;", "'")

    # Clean up whitespace
    text_content = re.sub(r"\s+", " ", text_content)
    text_content = text_content.strip()

    return text_content


def generate_summary(content: str, max_length: int = 200) -> str:
    """
    Generate a summary of content.

    Args:
        content: Full content text
        max_length: Maximum summary length

    Returns:
        Content summary
    """
    if len(content) <= max_length:
        return content

    # Try to find a good breaking point
    words = content.split()
    summary_words = words[: max_length // 5]  # Approximate word count

    summary = " ".join(summary_words)

    # Try to end at a sentence boundary
    sentence_end = summary.rfind(".")
    if sentence_end > max_length * 0.7:  # If we can end at a sentence
        summary = summary[: sentence_end + 1]

    return summary + "..."


def validate_llms_txt_content(content: str) -> Dict[str, Any]:
    """
    Validate LLMs.txt content for compliance.

    Args:
        content: Generated LLMs.txt content

    Returns:
        Validation results
    """
    validation = {"valid": True, "errors": [], "warnings": [], "compliance_score": 100}

    # Check for required elements
    if not content.startswith("# "):
        validation["errors"].append("Missing H1 title")
        validation["compliance_score"] -= 20

    if "> " not in content:
        validation["errors"].append("Missing blockquote description")
        validation["compliance_score"] -= 20

    if "## " not in content:
        validation["warnings"].append("No sections found")
        validation["compliance_score"] -= 10

    # Check for proper markdown structure
    if not re.search(r"## [^\n]+\n", content):
        validation["warnings"].append("Sections should use H2 headers")
        validation["compliance_score"] -= 5

    # Check for links
    if not re.search(r"\[([^\]]+)\]\(([^)]+)\)", content):
        validation["warnings"].append("No markdown links found")
        validation["compliance_score"] -= 5

    # Update validity
    if validation["errors"]:
        validation["valid"] = False
        validation["compliance_score"] = max(0, validation["compliance_score"])

    return validation


def format_llms_txt_metadata(metadata: Dict[str, Any]) -> str:
    """
    Format metadata for LLMs.txt files.

    Args:
        metadata: Metadata dictionary

    Returns:
        Formatted metadata string
    """
    lines = []

    if "generator" in metadata:
        lines.append(f"Generated by: {metadata['generator']}")

    if "generation_date" in metadata:
        lines.append(f"Generation date: {metadata['generation_date']}")

    if "source_urls" in metadata:
        lines.append(f"Source URLs: {', '.join(metadata['source_urls'])}")

    if "total_pages" in metadata:
        lines.append(f"Total pages: {metadata['total_pages']}")

    if "categories" in metadata:
        lines.append(f"Categories: {', '.join(metadata['categories'])}")

    return "\n".join(lines)


def cleanup_temp_files(temp_dir: str):
    """
    Clean up temporary files and directories.

    Args:
        temp_dir: Temporary directory path
    """
    try:
        temp_path = Path(temp_dir)
        if temp_path.exists():
            import shutil

            shutil.rmtree(temp_path)
            logger.info(f"🗑️ Cleaned up temporary directory: {temp_path}")
    except Exception as e:
        logger.warning(f"Could not cleanup temporary files: {e}")
