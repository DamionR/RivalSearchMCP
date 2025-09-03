"""
LLMs.txt Generator tools for FastMCP server.
Handles generation of LLMs.txt files for websites following the llmstxt.org specification.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup
from fastmcp import FastMCP

from src.logging.logger import logger


def register_llms_tools(mcp: FastMCP):
    """Register all LLMs.txt generator-related tools."""

    @mcp.tool
    async def generate_llms_txt(url: str) -> dict:
        """
        Generate LLMs.txt files for a website following the llmstxt.org specification.

        Args:
            url: Website URL to generate LLMs.txt for (supports various formats: https://example.com, example.com, @https://example.com, local file paths)

        Returns:
            Generation result with file details and content
        """
        try:
            logger.info(f"📝 Generating LLMs.txt for: {url}")

            # Normalize URL
            if url.startswith("@"):
                url = url[1:]
            if not url.startswith(("http://", "https://", "file://")):
                if os.path.exists(url):
                    url = f"file://{os.path.abspath(url)}"
                else:
                    url = f"https://{url}"

            # Create temporary output directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create configuration
                config = {
                    "name": "Website Documentation",
                    "description": f"Documentation generated from {url}",
                    "urls": [url],
                    "output_dir": temp_dir,
                    "max_pages": 100,
                    "max_depth": 3,
                    "traversal_mode": "docs",
                    "rate_limit": 1.0,
                    "user_agent": "LLMs.txt Generator/1.0",
                }

                # Initialize and run generator
                generator = LLMsTxtGenerator(config)
                generator.run()

                # Get generated files
                output_path = Path(temp_dir)
                txt_files = list(output_path.glob("*.txt"))
                json_files = list(output_path.glob("*.json"))
                all_files = txt_files + json_files

                # Read file contents for response
                files_data = {}
                for file in all_files:
                    try:
                        with open(file, "r", encoding="utf-8") as f:
                            files_data[file.name] = f.read()
                    except Exception as e:
                        logger.warning(f"Could not read {file.name}: {e}")

                # Copy files to current directory for user access
                for file in all_files:
                    shutil.copy2(file, ".")

                logger.info(f"✅ Successfully generated {len(all_files)} files")

                return {
                    "success": True,
                    "pages_processed": len(generator.pages_data),
                    "files_generated": [f.name for f in all_files],
                    "output_directory": os.getcwd(),
                    "files_content": files_data,
                }

        except Exception as e:
            logger.error(f"❌ Error generating LLMs.txt: {e}")
            return {
                "success": False,
                "error": str(e),
                "pages_processed": 0,
                "files_generated": [],
                "output_directory": "",
                "files_content": {},
            }


class LLMsTxtGenerator:
    """
    Generic LLMs.txt generator that can work with any documentation website.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the generator with a configuration.

        Args:
            config: Configuration dictionary containing:
                - name: Project name
                - description: Project description
                - urls: List of URLs to start crawling from
                - max_pages: Maximum number of pages to process
                - user_agent: User agent string
                - traversal_mode: Traversal mode - "docs", "research", "map"
        """
        self.config = config
        self.visited_urls = set()
        self.pages_data = []

        # Import here to avoid import issues
        import requests

        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": config.get("user_agent", "LLMs.txt Generator/1.0")}
        )

    def discover_pages(self) -> list:
        """Discover pages using simple link discovery."""
        discovered_pages = []
        base_urls = self.config.get("urls", [])
        max_pages = self.config.get("max_pages", 100)

        logger.info("Using simple page discovery")
        logger.info(f"Base URLs: {base_urls}")

        for base_url in base_urls:
            logger.info(f"Processing base URL: {base_url}")

            # Use simple link discovery to find pages
            discovered_urls = self._simple_link_discovery(base_url, max_pages)

            # Add the base URL itself if not already found
            if base_url not in discovered_urls:
                discovered_urls.insert(0, base_url)

            for url in discovered_urls:
                if len(discovered_pages) >= max_pages:
                    break
                if url not in [page["url"] for page in discovered_pages]:
                    discovered_pages.append({"url": url, "source": "link_discovery"})

        logger.info(f"Discovered {len(discovered_pages)} pages using simple discovery")
        return discovered_pages or []

    def _simple_link_discovery(self, base_url: str, max_pages: int) -> list:
        """Simple link discovery as fallback."""
        discovered_urls = []

        try:
            html_content = self.get_page_content(base_url)
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")

                # Find all links
                for link in soup.find_all("a", href=True):
                    try:
                        # Type cast to handle type checker
                        from bs4 import Tag

                        if isinstance(link, Tag):
                            href_attr = link["href"]
                            if href_attr and isinstance(href_attr, str):
                                full_url = self._resolve_url(base_url, href_attr)

                                if full_url and full_url not in discovered_urls:
                                    discovered_urls.append(full_url)
                                    if len(discovered_urls) >= max_pages:
                                        break
                    except (KeyError, TypeError):
                        continue
        except Exception as e:
            logger.warning(f"Link discovery failed for {base_url}: {e}")

        return discovered_urls

    def get_page_content(self, url: str) -> Optional[str]:
        """Get page content."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"Failed to get content from {url}: {e}")
            return None

    def _resolve_url(self, base_url: str, href: str) -> Optional[str]:
        """Resolve relative URLs to absolute URLs."""
        try:
            from urllib.parse import urljoin, urlparse

            # Skip external links, javascript, mailto, etc.
            if href.startswith(
                ("http://", "https://", "javascript:", "mailto:", "tel:")
            ):
                return None

            # Resolve relative URL
            full_url = urljoin(base_url, href)

            # Only include same-domain URLs
            base_domain = urlparse(base_url).netloc
            full_domain = urlparse(full_url).netloc

            if base_domain == full_domain:
                return full_url

            return None
        except Exception:
            return None

    def process_pages(self, discovered_pages: list):
        """Process discovered pages to extract content."""
        logger.info("Starting page processing...")

        for i, page_info in enumerate(discovered_pages, 1):
            url = page_info["url"]

            if url in self.visited_urls:
                continue

            logger.info(f"Processing page {i}/{len(discovered_pages)}: {url}")

            try:
                content = self.get_page_content(url)
                if content:
                    soup = BeautifulSoup(content, "html.parser")

                    # Extract title
                    title_tag = soup.find("title")
                    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

                    # Extract main content
                    main_content = self._extract_main_content(soup)

                    # Clean content
                    clean_content = self._clean_content(main_content)

                    # Categorize page
                    category = self._categorize_page(title, clean_content, url)

                    # Store page data
                    self.pages_data.append(
                        {
                            "url": url,
                            "title": title,
                            "content": clean_content,
                            "category": category,
                            "description": (
                                clean_content[:200] + "..."
                                if len(clean_content) > 200
                                else clean_content
                            ),
                        }
                    )

                    self.visited_urls.add(url)

            except Exception as e:
                logger.warning(f"Failed to process {url}: {e}")

        logger.info(f"Processed {len(self.pages_data)} pages")

    def _extract_main_content(self, soup) -> str:
        """Extract main content from HTML."""
        # Try to find main content areas
        main_selectors = [
            "main",
            '[role="main"]',
            ".main-content",
            ".content",
            ".post-content",
            ".article-content",
            "#content",
            "#main",
        ]

        for selector in main_selectors:
            main_element = soup.select_one(selector)
            if main_element:
                return str(main_element)

        # Fallback: remove navigation and get body content
        self._remove_unwanted_elements(soup)
        body = soup.find("body")
        if body:
            return str(body)

        return str(soup)

    def _remove_unwanted_elements(self, soup):
        """Remove unwanted HTML elements."""
        import re

        # Remove script and style elements
        for element in soup(
            ["script", "style", "noscript", "iframe", "embed", "object"]
        ):
            element.decompose()

        # Remove navigation, footer, header elements
        for element in soup(["nav", "footer", "header", "aside", "menu"]):
            element.decompose()

        # Remove common ad and tracking elements
        for element in soup.find_all(
            class_=re.compile(
                r"(ad|ads|advertisement|banner|tracking|analytics|cookie|popup|modal|overlay)",
                re.I,
            )
        ):
            element.decompose()

    def _clean_content(self, content: str) -> str:
        """Clean and format content."""
        import re

        # Remove extra whitespace
        content = re.sub(r"\s+", " ", content)

        # Remove HTML tags
        content = re.sub(r"<[^>]+>", "", content)

        # Clean up text
        content = content.strip()

        return content

    def _categorize_page(self, title: str, content: str, url: str) -> str:
        """Categorize page based on content and URL."""
        title_lower = title.lower()
        content.lower()
        url_lower = url.lower()

        # Documentation categories
        if any(
            word in title_lower
            for word in ["api", "reference", "docs", "documentation"]
        ):
            return "API Reference"
        elif any(
            word in title_lower
            for word in ["guide", "tutorial", "how-to", "getting started"]
        ):
            return "Guides & Tutorials"
        elif any(word in title_lower for word in ["example", "sample", "demo"]):
            return "Examples & Demos"
        elif any(word in title_lower for word in ["install", "setup", "configuration"]):
            return "Installation & Setup"
        elif any(
            word in title_lower
            for word in ["faq", "help", "support", "troubleshooting"]
        ):
            return "Help & Support"
        elif any(word in url_lower for word in ["blog", "news", "announcement"]):
            return "Blog & News"
        else:
            return "Other"

    def generate_llms_txt(self, output_file: Path):
        """Generate llms.txt file following the llmstxt.org specification."""
        logger.info(f"Generating {output_file}...")

        # Group pages by category
        categories = {}
        for page in self.pages_data:
            category = page["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(page)

        with open(output_file, "w", encoding="utf-8") as f:
            # Write H1 title (required)
            f.write(f"# {self.config['name']}\n\n")

            # Write blockquote summary (required)
            f.write(f"> {self.config['description']}\n\n")

            # Write sections with H2 headers and full content
            for category in sorted(categories.keys()):
                if category == "Other":
                    # Use "Optional" for the "Other" category as per spec
                    f.write("## Optional\n\n")
                else:
                    f.write(f"## {category}\n\n")

                for page in sorted(categories[category], key=lambda x: x["title"]):
                    # Write the link first (following llmstxt.org format)
                    description = page["description"] if page["description"] else ""
                    f.write(f"- [{page['title']}]({page['url']})")
                    if description:
                        f.write(f": {description}")
                    f.write("\n\n")

                    # Write the full content
                    f.write(page["content"])
                    f.write("\n\n---\n\n")

        logger.info(
            f"Generated {output_file} with full content from {len(self.pages_data)} pages"
        )

    def generate_llms_full_txt(self, output_file: Path):
        """Generate llms-full.txt file with expanded content."""
        logger.info(f"Generating {output_file}...")

        # Group pages by category
        categories = {}
        for page in self.pages_data:
            category = page["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(page)

        with open(output_file, "w", encoding="utf-8") as f:
            # Write H1 title (required)
            f.write(f"# {self.config['name']}\n\n")

            # Write blockquote summary (required)
            f.write(f"> {self.config['description']}\n\n")

            # Write sections with H2 headers and full content
            for category in sorted(categories.keys()):
                if category == "Other":
                    # Use "Optional" for the "Other" category as per spec
                    f.write("## Optional\n\n")
                else:
                    f.write(f"## {category}\n\n")

                for page in sorted(categories[category], key=lambda x: x["title"]):
                    # Write the link first (following llmstxt.org format)
                    description = page["description"] if page["description"] else ""
                    f.write(f"- [{page['title']}]({page['url']})")
                    if description:
                        f.write(f": {description}")
                    f.write("\n\n")

                    # Write the full content
                    f.write(page["content"])
                    f.write("\n\n---\n\n")

        logger.info(
            f"Generated {output_file} with full content from {len(self.pages_data)} pages"
        )

    def save_data(self, output_file: Path):
        """Save raw data for debugging."""
        import json

        with open(output_file, "w") as f:
            json.dump(self.pages_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved raw data to {output_file}")

    def run(self):
        """Main execution method."""
        logger.info(f"LLMs.txt Generator for {self.config['name']}")
        logger.info("=" * 50)

        # Discover pages
        logger.info("Starting page discovery...")
        discovered_pages = self.discover_pages()
        logger.info(f"\nDiscovered {len(discovered_pages)} pages")

        # Process pages
        logger.info("Starting page processing...")
        self.process_pages(discovered_pages)

        # Generate output files following llmstxt.org specification
        logger.info("Starting file generation...")
        output_dir = self.config.get("output_dir", ".")

        # Generate files in the specified output directory
        self.generate_llms_txt(Path(output_dir) / "llms.txt")
        self.generate_llms_full_txt(Path(output_dir) / "llms-full.txt")
        self.save_data(Path(output_dir) / "documentation_data.json")

        logger.info("\nGeneration complete!")
        logger.info(f"Processed {len(self.pages_data)} pages")
        logger.info("Generated files:")
        logger.info("- llms.txt (standard llmstxt.org format)")
        logger.info("- llms-full.txt (full content with expanded links)")
        logger.info("- documentation_data.json (raw data)")
