#!/usr/bin/env python3
"""
OCR processing component for RivalSearchMCP.
Handles OCR processing of images from web content.
"""

import asyncio
import httpx
from typing import List, cast
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse

from src.logger import logger


async def process_images_ocr(soup: BeautifulSoup, base_url: str) -> List[str]:
    """
    Process images in HTML content using OCR to extract text.
    
    Args:
        soup: BeautifulSoup object containing HTML
        base_url: Base URL for resolving relative image URLs
        
    Returns:
        List of extracted text strings from images
    """
    images = []
    for img in soup.find_all('img'):
        img_tag = cast(Tag, img)
        src = img_tag.get('src', '')
        if src:
            images.append(src)
    
    async def ocr_img(img_src: str) -> str:
        """Process a single image with OCR."""
        img_url = urlparse(base_url)._replace(path=img_src).geturl() if not img_src.startswith('http') else img_src
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(img_url, timeout=10)
            img = Image.open(BytesIO(resp.content))
            return image_to_string(img)
        except Exception as e:
            logger.debug(f"OCR failed for {img_url}: {e}")
            return ""
    
    tasks = [ocr_img(src) for src in images]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions and empty results
    valid_results = []
    for result in results:
        if isinstance(result, Exception):
            logger.debug(f"OCR task failed: {result}")
        elif isinstance(result, str) and result.strip():
            valid_results.append(result.strip())
    
    return valid_results
