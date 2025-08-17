import re
from typing import List, Tuple, Dict
from bs4 import BeautifulSoup

def extract_triples(text: str) -> List[Tuple[str, str, str]]:
    triples = []
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 2:
            subject = words[0]
            predicate = words[1]
            obj = ' '.join(words[2:])
            triples.append((subject, predicate, obj))
    return triples

def extract_search_results(html: str, max_results: int = 10) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    seen_urls = set()
    selector_sets = [
        {'container': '#search div[data-hveid]', 'title': 'h3', 'snippet': '.VwiC3b'},
        {'container': '#rso div[data-hveid]', 'title': 'h3', 'snippet': '[data-sncf="1"]'},
        {'container': '.g', 'title': 'h3', 'snippet': 'div[style*="webkit-line-clamp"]'},
        {'container': 'div[jscontroller][data-hveid]', 'title': 'h3', 'snippet': 'div[role="text"]'}
    ]
    alt_snippet_selectors = ['.VwiC3b', '[data-sncf="1"]', 'div[style*="webkit-line-clamp"]', 'div[role="text"]']

    for selectors in selector_sets:
        if len(results) >= max_results:
            break
        containers = soup.select(selectors['container'])
        for container in containers:
            if len(results) >= max_results:
                break
            title_elem = container.select_one(selectors['title'])
            if not title_elem:
                continue
            title = title_elem.text.strip()
            link = ''
            link_in_title = title_elem.find_parent('a')
            if link_in_title and hasattr(link_in_title, 'get'):  # type: ignore
                link = link_in_title.get('href', '')  # type: ignore
            else:
                parent = title_elem.parent
                while parent and parent.name != 'a':
                    parent = parent.parent
                if parent and parent.name == 'a' and hasattr(parent, 'get'):  # type: ignore
                    link = parent.get('href', '')  # type: ignore
                else:
                    container_link = container.find('a')  # type: ignore
                    if container_link and hasattr(container_link, 'get'):  # type: ignore
                        link = container_link.get('href', '')  # type: ignore
                    else:
                        link = ''
            if not link or not isinstance(link, str) or not link.startswith('http') or link in seen_urls:
                continue
            snippet = ''
            snippet_elem = container.select_one(selectors['snippet'])
            if snippet_elem:
                snippet = snippet_elem.text.strip()
            else:
                for alt in alt_snippet_selectors:
                    elem = container.select_one(alt)
                    if elem:
                        snippet = elem.text.strip()
                        break
                if not snippet:
                    text_divs = [div for div in container.find_all('div') if not div.find('h3') and len(div.text.strip()) > 20]  # type: ignore
                    if text_divs:
                        snippet = text_divs[0].text.strip()
            if title and link:
                results.append({'title': title, 'link': link, 'snippet': snippet})
                seen_urls.add(link)

    if len(results) < max_results:
        anchors = soup.select("a[href^='http']")
        for a in anchors:
            if len(results) >= max_results:
                break
            link = a.get('href', '') if hasattr(a, 'get') else ''  # type: ignore
            if not link or not isinstance(link, str) or not link.startswith('http') or 'google.com' in link or link in seen_urls:
                continue
            title = a.text.strip()
            if not title:
                continue
            snippet = ''
            parent = a.parent
            for _ in range(3):
                if parent:
                    text = parent.text.strip()
                    if len(text) > 20 and text != title:
                        snippet = text
                        break
                    parent = parent.parent
            results.append({'title': title, 'link': link, 'snippet': snippet})
            seen_urls.add(link)

    return results[:max_results]
