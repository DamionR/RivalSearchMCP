import asyncio
import httpx
from typing import List
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string
from bs4 import BeautifulSoup
from urllib.parse import urlparse

async def process_images_ocr(soup: BeautifulSoup, base_url: str) -> List[str]:
    images = [img.get('src', '') for img in soup.find_all('img') if img.get('src')]  # type: ignore
    
    async def ocr_img(img_src):
        img_url = urlparse(base_url)._replace(path=img_src).geturl() if not img_src.startswith('http') else img_src
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(img_url, timeout=10)
            img = Image.open(BytesIO(resp.content))
            return image_to_string(img)
        except Exception:
            return ""
    tasks = [ocr_img(src) for src in images]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r]
