import os

DEFAULT_UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
]

PAYWALL_INDICATORS = ["subscribe", "paywall", "sign in to read", "become a member", "login to continue"]

ARCHIVE_FALLBACKS = ["https://archive.is/?url=", "https://12ft.io/proxy?q=", "https://webcache.googleusercontent.com/search?q=cache:"]

def get_config():
    return {
    
        'suppress_logs': os.environ.get('SUPPRESS_LOGS', 'false').lower() == 'true',
    }
