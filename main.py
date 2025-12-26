import httpx
from urllib.parse import urljoin, urlparse
from crawler.frontier import URLFrontier
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawler.frontier import URLFrontier
from main_fetcher import fetch

def extract_links(base_url, html):
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.find_all("a", href = True):
        absolute_url = urljoin(base_url, a["href"])
        links.append(absolute_url)
    return links

def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc

def fetch_robots_txt(base_url: str) -> str:
    """
    Fetch robots.txt for given url and return content
    """
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    print(f"Fetching robots.txt from {robots_url}")

    r = fetch(robots_url)
    if r.status_code == 200:
        return r.text
    else:
        print(f"No robots.txt found or blocked (status {r.status_code})")
        return ""



def main():
    base_url = "https://books.toscrape.com"
    frontier = URLFrontier(base_url)

    frontier.add_url(base_url, depth=0)

    # Crawl loop
    while frontier.has_urls():
        url, depth = frontier.get_next()
        if (url is None) or (depth > 2):
            continue

        print(f"Crawling {url} at depth {depth}")
        r = fetch(url)
        if r.status_code == 200:
            html = r.text
            print(html[:100])

            # Extract links
            links = extract_links(url, html)
            for link in links:
                frontier.add_url(link, depth=depth + 1)

    robots_content = fetch_robots_txt(base_url)
    print("robots.txt preview:")
    print(robots_content[:300], "\n")

    r = fetch(base_url)

    print(r.status_code)
    print(r.text[:100])

if __name__ == "__main__":
    main()