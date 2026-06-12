import requests

from bs4 import BeautifulSoup
from bs4 import Comment
import re
from urllib.parse import urljoin
from urllib.parse import urlparse
from collections import deque


# URLs we don't want to crawl

BLOCKED_KEYWORDS = [

    "login",
    "register",
    "signup",
    "signin",
    "cart",
    "checkout",
    "account",
    "wp-admin"

]

def fetch_page(url):

    try:

        response = requests.get(

            url,

            timeout=10,

            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        return response.text

    except Exception as e:

        print(e)

        return None
    
def extract_content(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Remove unwanted elements

    remove_tags = [

        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "canvas",
        "footer",
        "header",
        "nav",
        "form",
        "button"
    ]

    for tag in remove_tags:

        for element in soup.find_all(tag):

            element.decompose()


    # Remove HTML comments

    comments = soup.find_all(

        string=lambda text:
        isinstance(text, Comment)
    )

    for comment in comments:

        comment.extract()


    # Title

    title = ""

    if soup.title:

        title = soup.title.get_text(
            strip=True
        )


    content_parts = []


    # Headings

    for heading in soup.find_all(

        [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6"
        ]
    ):

        text = heading.get_text(
            " ",
            strip=True
        )

        if len(text) > 2:

            content_parts.append(
                f"\n{text}\n"
            )


    # Paragraphs

    for paragraph in soup.find_all("p"):

        text = paragraph.get_text(
            " ",
            strip=True
        )

        if len(text) > 20:

            content_parts.append(
                text
            )


    # Lists

    for li in soup.find_all("li"):

        text = li.get_text(
            " ",
            strip=True
        )

        if len(text) > 5:

            content_parts.append(
                f"• {text}"
            )


    # Tables

    for row in soup.find_all("tr"):

        cols = [

            td.get_text(
                " ",
                strip=True
            )

            for td in row.find_all(
                [
                    "td",
                    "th"
                ]
            )
        ]

        if cols:

            content_parts.append(
                " | ".join(cols)
            )


    content = "\n".join(
        content_parts
    )


    content = re.sub(

        r"\s+",

        " ",

        content
    )

    content = content.strip()


    return {

        "title": title,

        "content": content
    }
    
def get_internal_links(

    html,

    base_url
):

    soup = BeautifulSoup(

        html,

        "html.parser"
    )

    links = set()

    base_domain = urlparse(
        base_url
    ).netloc


    for tag in soup.find_all(

        "a",

        href=True
    ):

        href = tag["href"]

        full_url = urljoin(

            base_url,

            href
        )

        parsed = urlparse(
            full_url
        )

        if parsed.netloc == base_domain:

            links.add(

                parsed.scheme
                + "://"
                + parsed.netloc
                + parsed.path
            )

    return list(
        links
    )
    
def crawl_website(
    website_url,
    max_pages=100
):

    visited = set()

    queue = deque()

    pages = []

    sitemap_urls = get_sitemap_urls(
        website_url
    )

    if sitemap_urls:

        queue.extend(
            sitemap_urls
        )

    else:

        queue.append(
            website_url
        )

    while queue and len(visited) < max_pages:

        current_url = queue.popleft()

        if current_url in visited:

            continue

        if should_skip_url(
            current_url
        ):

            continue

        print(
            f"Crawling: {current_url}"
        )

        visited.add(
            current_url
        )

        html = fetch_page(
            current_url
        )

        if not html:

            continue

        data = extract_content(
            html
        )

        pages.append({

            "url": current_url,

            "title": data["title"],

            "content": data["content"]

        })

        new_links = get_internal_links(

            html,

            current_url

        )

        for link in new_links:

            if link not in visited:

                queue.append(
                    link
                )

    return pages



def get_sitemap_urls(base_url):

    sitemap_url = base_url.rstrip("/") + "/sitemap.xml"

    try:

        response = requests.get(
            sitemap_url,
            timeout=10
        )

        if response.status_code != 200:

            return []

        soup = BeautifulSoup(
            response.text,
            "xml"
        )

        urls = []

        for loc in soup.find_all("loc"):

            urls.append(
                loc.text.strip()
            )

        return urls

    except Exception:

        return []
    
def should_skip_url(url):

    url = url.lower()

    for keyword in BLOCKED_KEYWORDS:

        if keyword in url:

            return True

    return False