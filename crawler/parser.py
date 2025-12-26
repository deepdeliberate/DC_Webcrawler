from bs4 import BeautifulSoup

def parse_wiki_page(html):
    soup = BeautifulSoup(html, "lxml")
    title_tag = soup.find("h1", id = "firstHeading")
    content_div = soup.find("div", id="mw-content-text")

    title = title_tag.text.strip() if title_tag else "No Title"
    summary = ""
    if content_div:
        for p in content_div.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                summary = text
                break
    
    return {
        "title": title,
        "summary": summary
    }