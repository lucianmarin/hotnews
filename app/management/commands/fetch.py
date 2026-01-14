from datetime import datetime, timezone

import feedparser
import requests
from app.filters import hostname
from app.helpers import fetch_content, get_url, load_articles, save_articles, md5
from dateutil.parser import parse
from django.core.management.base import BaseCommand
from project.settings import FEEDS


class Command(BaseCommand):
    help = "Fetch articles from feeds."
    ignored = [
        "https://kottke.org/quick-links"
    ]
    articles = {}

    @property
    def now(self):
        return datetime.now(timezone.utc).timestamp()

    @property
    def cutoff(self):
        return self.now - 48 * 3600

    def get_entries(self, feed):
        r = requests.get(feed)
        print(feed)
        entries = feedparser.parse(r.text).entries
        print(len(entries), "entries found")
        for entry in entries:
            try:
                origlink = entry.get('feedburner_origlink')
                entry.link = origlink if origlink else entry.link
                url = get_url(entry.link)
                published = parse(entry.published).timestamp()
                if self.now > published > self.cutoff and url not in self.ignored:
                    key = md5(url)
                    if key not in self.articles:
                        self.articles[key] = {
                            'id': key,
                            'base': key,
                            'url': url,
                            'title': entry.title,
                            'domain': hostname(url),
                            'pub': published,
                            'author': getattr(entry, 'author', ''),
                            'description': None,
                            'score': 0,
                            'paragraphs': [],
                            'ips': []
                        }
                        print('Created', url)
            except Exception as e:
                print(e)

    def grab_entries(self):
        for feed in FEEDS:
            self.get_entries(feed)

    def cleanup(self):
        keys_to_delete = [k for k, v in self.articles.items() if v['pub'] < self.cutoff]
        for k in keys_to_delete:
            del self.articles[k]
        print("Deleted {0} entries".format(len(keys_to_delete)))

    def get_content(self, key):
        article = self.articles.get(key)

        if not article:
            return

        description, paragraphs = fetch_content(article['url'])

        if key in self.articles:
            self.articles[key]['description'] = description
            self.articles[key]['paragraphs'] = paragraphs
            print('Read', article['url'], len(paragraphs))
            print(article['description'])

    def grab_content(self):
        keys_to_fetch = [k for k, v in self.articles.items() if not v.get('description')]
        for key in keys_to_fetch:
            self.get_content(key)

    def handle(self, *args, **options):
        self.articles = load_articles()
        self.grab_entries()
        self.cleanup()
        self.grab_content()
        save_articles(self.articles)
