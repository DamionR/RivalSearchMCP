"""
Retrieval tools for FastMCP server.
Handles content retrieval, streaming, batch operations, and image extraction.
"""

from typing import List, Union

from fastmcp import FastMCP

from src.core.fetch import (
    base_fetch_url,
    batch_rival_retrieve,
    rival_retrieve,
    stream_fetch,
)
# TODO: Implement image OCR
# from src.core.search import process_images_ocr
from src.logging.logger import logger
from src.utils import clean_html_to_markdown


def register_retrieval_tools(mcp: FastMCP):
    """Register all retrieval-related tools."""

    @mcp.tool
    async def retrieve_content(
        resource: Union[str, List[str]], limit: int = 5, extract_images: bool = False
    ) -> dict:
        """
        Enhanced content retrieval with support for single/multiple resources and image extraction.

        Args:
            resource: Single URL, list of URLs, or search query (e.g., "search:python")
            limit: Maximum number of results for batch operations
            extract_images: Whether to extract and process images with OCR
        """
        try:
            logger.info(f"Retrieving content from: {resource}")

            # Handle list of resources (batch retrieval)
            if isinstance(resource, list):
                logger.info(f"Batch retrieving from {len(resource)} resources")
                results = await batch_rival_retrieve(resource, max_concurrent=limit)

                # Extract content from results
                content_parts = []
                for result in results:
                    if result.get("success") and result.get("content"):
                        # Clean HTML and format content
                        content_str = (
                            str(result["content"]) if result["content"] else ""
                        )
                        clean_content = clean_html_to_markdown(
                            content_str, result.get("url", "")
                        )
                        content_parts.append(clean_content)

                combined_content = "\n\n---\n\n".join(content_parts)

                return {
                    "success": True,
                    "content": combined_content,
                    "url": ", ".join(resource),
                    "is_search": False,
                    "method": "batch_retrieval",
                }

            # Handle single resource
            else:
                # Check if it's a search query
                is_search = resource.startswith("search:")

                if is_search:
                    # Use the existing rival_retrieve function for search queries
                    search_results = await rival_retrieve(resource, limit)
                    # rival_retrieve already returns clean content for search queries
                    clean_content = str(search_results) if search_results else ""
                else:
                    # Use base_fetch_url for direct URLs
                    content = await base_fetch_url(resource)

                    if not content:
                        return {
                            "success": False,
                            "error": f"Failed to retrieve content from {resource}",
                            "url": resource,
                            "is_search": is_search,
                        }

                    # Clean HTML and format content
                    content_str = str(content) if content else ""
                    clean_content = clean_html_to_markdown(content_str, resource)

                # Handle image extraction if requested
                if extract_images and not is_search:
                    try:
                        from bs4 import BeautifulSoup

                        content_for_soup = content if content else ""
                        soup = BeautifulSoup(str(content_for_soup), "html.parser")
                        # TODO: Implement image OCR
                        # ocr_results = await process_images_ocr(soup, resource)
                        
                        # For now, just add a placeholder
                        clean_content += "\n\n**Image extraction not yet implemented**"
                    except Exception as e:
                        logger.warning(f"Image extraction failed: {e}")

                return {
                    "success": True,
                    "content": clean_content,
                    "url": resource,
                    "is_search": is_search,
                    "method": "single_retrieval",
                }

        except Exception as e:
            logger.error(f"Content retrieval failed for {resource}: {e}")
            return {
                "success": False,
                "error": str(e),
                "url": resource,
                "is_search": isinstance(resource, str)
                and resource.startswith("search:"),
            }

    @mcp.tool
    async def stream_content(url: str) -> dict:
        """Retrieve streaming content from WebSocket URLs."""
        try:
            logger.info(f"Retrieving stream from: {url}")
            content = await stream_fetch(url)

            # Clean and format streaming content
            clean_content = clean_html_to_markdown(str(content) if content else "", url)

            return {
                "success": True,
                "content": clean_content,
                "url": url,
                "is_search": False,
                "method": "stream_retrieval",
            }
        except Exception as e:
            logger.error(f"Stream retrieval failed for {url}: {e}")
            return {"success": False, "error": str(e), "url": url, "is_search": False}
