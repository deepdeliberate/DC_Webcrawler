import httpx

HEADERS = {
    "User-Agent": "SimpleCrawler/0.1 (+https://example.com/bot-info)",
    "Accept": "text/html",
}

def fetch(url: str) -> httpx.Response:
    with httpx.Client(headers=HEADERS, timeout=10, follow_redirects=True) as client:
        return client.get(url)