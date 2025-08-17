from .fetch import base_fetch_url, batch_rival_retrieve, stream_fetch
from .bypass import get_proxies, refresh_proxies, detect_paywall, select_ua, select_proxy
from .extract import extract_triples, extract_search_results
from .multi_modal import process_images_ocr

__all__ = [
    'base_fetch_url',
    'batch_rival_retrieve', 
    'stream_fetch',
    'get_proxies',
    'refresh_proxies',
    'detect_paywall',
    'select_ua',
    'select_proxy',
    'extract_triples',
    'extract_search_results',
    'process_images_ocr'
]
