from .models import WebsitePage
from .scraper import crawl_website


def crawl_and_save(chatbot):

    pages = crawl_website(
        chatbot.website_url
    )

    print(
        f"Found {len(pages)} pages"
    )

    chatbot.pages.all().delete()

    for page_data in pages:

        WebsitePage.objects.create(

            chatbot=chatbot,

            url=page_data["url"],

            title=page_data["title"],

            content=page_data["content"]
        )

    print(
        "Pages saved successfully"
    )