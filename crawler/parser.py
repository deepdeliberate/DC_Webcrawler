from bs4 import BeautifulSoup

def parse_wiki_page(html):
    soup = BeautifulSoup(html, "lxml")
    title_tag = soup.find("h1", id = "firstHeading")
    content_div = soup.find("div", id="mw-context-text")

    title = title_tag.text.strip() if title_tag else "No Title"
    summary = ""
    if content_div:
        p = content_div.find("p")
        if p:
            summary = p.text.strip()
    
    return {
        "title": title,
        "summary": summary
    }