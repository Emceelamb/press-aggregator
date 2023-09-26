from django.core.management.base import BaseCommand, CommandError
from web.models import Article

import pprint
import requests
from ..scraper.rss import get_feed, get_url, scrape_page
from ..scraper.topic_extraction import get_topics, sanitize_text

pp = pprint.PrettyPrinter(indent=4)


class Command(BaseCommand):
    help = "Scrapes articles"

    def handle(self, *args, **options):
        print("Scraping rss...")

        url = "http://fetchrss.com/rss/6508da2a6f4dc52d890085e26511ef5c91c5b47177669bf3.xml"
        # url = "https://fetchrss.com/rss/6508da2a6f4dc52d890085e26508d97829ab1e4f05782d42.xml"

        feed = get_feed(url)
        print(feed)
        articles = []

        for document in feed["articles"]:
            # print(document)
            # link = get_url(document.links)
            article = {
                "title": document["title"],
                "link": document["link"],
                "agency": feed["agency"],
            }
            articles.append(article)

        for article in articles:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
            }
            page = requests.get(article["link"], headers=headers)
            print(article["link"])

            content = scrape_page(page)
            print("\n\033[31mScraped content:\033[0m")
            pp.pprint(content)

            tokens = sanitize_text(content)
            print("\n\033[31mTokens:\033[0m")
            pp.pprint(tokens)

            topics = get_topics(tokens)
            print("\n\033[31mTopics:\033[0m")
            pp.pprint(topics)
            article["topics"] = topics

        for a in articles:
            article = Article.objects.create(
                title=a["title"], agency=a["agency"], link=a["link"]
            )
            for tag in a["topics"]:
                print(tag)
                article.tags.add(tag)
            # pp.pprint({"title": a["title"], "topics": a["topics"]})
            print(article.tags.all())
            # article.save()
            print("Saving article")
