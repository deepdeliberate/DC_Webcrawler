import httpx
import json
import time

from urllib.parse import urljoin, urlparse
from crawler.frontier import URLFrontier
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawler.frontier import URLFrontier
from crawler import parser
from main_fetcher import fetch




def extract_links(base_url, html):
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.find_all("a", href = True):
        absolute_url = urljoin(base_url, a["href"])
        links.append(absolute_url)
    return links

def is_allowed_path(url, allowed_prefix = "/wiki/"):
    return urlparse(url).path.startswith(allowed_prefix)

def is_allowed_domain(base_url, target_url):
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
    # base_url = "https://books.toscrape.com"
    base_url = "https://www.detectiveconanworld.com/"
    frontier = URLFrontier(base_url)

    frontier.add_url("wiki/", depth=0)

    max_depth = 2
    crawl_delay = 1
    all_pages = []

    max_pages = 10
    crawled_pages = 0

    # Crawl loop
    while frontier.has_urls() and crawled_pages < max_pages:
        url, depth = frontier.get_next()
        if (url is None) or (depth > max_depth):
            continue

        if not is_allowed_domain(base_url, url) or not is_allowed_path(url):
            continue


        print(f"Crawling {url} at depth {depth}")
        try:
            r = fetch(url)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        if r.status_code == 200:
            data = parser.parse_wiki_page(r.text)
            data["url"] = url
            all_pages.append(data)
            html = r.text
            print(f"-> found page: {data['title']}")

            # Extract links
            links = extract_links(url, html)
            for link in links:
                if is_allowed_domain(base_url, link) and is_allowed_path(link):
                    frontier.add_url(link, depth=depth + 1)
        
        # Politeness
        time.sleep(crawl_delay)
        crawled_pages += 1

    with open("wiki_pages.json", "w", encoding="utf-8") as f:
        json.dump(all_pages, f, ensure_ascii = False, indent = 2)
    print(f"\nCrawled {len(all_pages)} pages. Results saved to wiki_pages.json")


if __name__ == "__main__":
    main()