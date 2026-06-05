import requests

from bs4 import BeautifulSoup
from bs4 import Comment
import re
from urllib.parse import urljoin
from urllib.parse import urlparse

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
    max_pages=20
):

    html = fetch_page(
        website_url
    )

    if not html:

        return []

    links = get_internal_links(

        html,

        website_url
    )

    pages = []

    for link in links[:max_pages]:

        print(
            f"Crawling: {link}"
        )

        page_html = fetch_page(
            link
        )

        if not page_html:

            continue

        data = extract_content(
            page_html
        )

        pages.append({

            "url": link,

            "title": data["title"],

            "content": data["content"]
        })

    return pages