#!/usr/bin/env python
import asyncio

import aiohttp
import feedparser
import favicon

from app.filters import hostname
from app.helpers import get_url
from app.settings import FEEDS, HEADERS


class FaviconFetcher:
    def __init__(self):
        self.urls = set()

    async def grab_feed_entries(self, session, feed):
        try:
            async with session.get(feed, timeout=10) as response:
                text = await response.text()
            print(feed)
            return feedparser.parse(text).entries
        except Exception as e:
            print(f"Error fetching feed {feed}: {e}")
            return []

    async def grab_entries(self):
        entries = []
        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(
                *(self.grab_feed_entries(session, feed) for feed in FEEDS),
                return_exceptions=True,
            )
        for result in results:
            if isinstance(result, Exception):
                print(f"Error collecting feed entries: {result}")
                continue
            entries += result

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
                icons = [i for i in favicon.get(url, headers=HEADERS) if i.format == 'png']
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
    asyncio.run(fetcher.grab_entries())
    fetcher.fetch()
