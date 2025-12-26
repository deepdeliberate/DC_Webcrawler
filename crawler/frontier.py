from collections import deque
from urllib.parse import urljoin, urlparse
import urllib.robotparser

class URLFrontier:
    def __init__(self, base_url):
        self.base_url = base_url
        self.queue = deque()
        self.seen = set()
        self.max_depth = 2
        self.robots_parser = urllib.robotparser.RobotFileParser()

        self._init_robots()

    def _init_robots(self):
        robots_url = urljoin(self.base_url, "/robots.txt")
        print(f"Fetching robots.txt from {robots_url}")
        self.robots_parser.set_url(robots_url)
        try:
            self.robots_parser.read()
        except Exception:
            print("Failed to read robots.txt, defaulting to allow all")
    
    def add_url(self, url, depth = 0):
        """Add URL To frontier if not seen and allowed by robots.txt"""
        normalized_url = urljoin(self.base_url, url)
        if normalized_url not in self.seen:
            self.queue.append((normalized_url, depth))
            self.seen.add(normalized_url)

    def get_next(self):
        """Pop the next URL from the frontier"""
        if self.queue:
            return self.queue.popleft()
        return None, None
    
    def has_urls(self):
        return bool(self.queue)