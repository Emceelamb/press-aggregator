from pprint import pp
import requests
from django.apps import apps
from rss import get_feed, get_url, scrape_page
from topic_extraction import get_topics, sanitize_text

Article = apps.get_model("web", "Article")


def main():
    feed = get_feed(url)
    articles = []

    for document in feed["articles"]:
        link = get_url(document.links)
        article = {"title": document["title"], "link": link, "agency": feed["agency"]}
        articles.append(article)

    for article in articles:
        page = requests.get(article["link"])
        content = scrape_page(page)
        tokens = sanitize_text(content)
        topics = get_topics(tokens)
        article["topics"] = topics

    for a in articles:
        article = Article(
            {
                "title": a["title"],
                "agency": a["agency"],
            }
        )
        for tag in article["tags"]:
            article.tags.add(tag)
        # pp.pprint({"title": a["title"], "topics": a["topics"]})
        print(Article)


# tokens = sanitize_text(content)
# topics = get_topics(tokens)


# pp.pprint(topics)

main()
