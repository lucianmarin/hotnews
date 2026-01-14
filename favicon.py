#!/usr/bin/env python
import feedparser
import requests
import favicon

from app.filters import hostname
from app.helpers import get_url
from project.settings import FEEDS


class FaviconFetcher:
    def __init__(self):
        self.urls = set()

    def grab_entries(self):
        entries = []
        for feed in FEEDS:
            try:
                r = requests.get(feed)
                entries += feedparser.parse(r.text).entries
                print(feed)
            except Exception as e:
                print(f"Error fetching feed {feed}: {e}")

        links = {}
        for entry in entries:
            try:
                origlink = entry.get('feedburner_origlink')
                entry.link = origlink if origlink else entry.link
                url = get_url(entry.link)
                domain = hostname(url)
                if domain not in links:
                    links[domain] = url
            except Exception as e:
                print(e)
        self.urls = set(links.values())

    def fetch(self):
        for url in self.urls:
            try:
                icons = [i for i in favicon.get(url) if i.format == 'png']
                print('---', '\n', url)
                if icons:
                    icon = icons[0]
                    print(icon.url)
                    print(icon.format, icon.width, icon.height)
                else:
                    print('missing')
            except Exception as e:
                print(f"Error fetching favicon for {url}: {e}")


if __name__ == "__main__":
    fetcher = FaviconFetcher()
    fetcher.grab_entries()
    fetcher.fetch()
