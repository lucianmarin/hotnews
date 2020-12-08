from datetime import datetime, timezone

import feedparser
import requests
from dateutil.parser import parse
from django.core.management.base import BaseCommand

from app.filters import hostname
from app.helpers import fetch_desc, fetch_fb, get_url
from app.models import Article
from project.settings import FEEDS
import favicon
from collections import defaultdict


class Command(BaseCommand):
    help = "Fetch favicons from websites."
    urls = set()

    def grab_entries(self):
        entries = []
        for feed in FEEDS:
            r = requests.get(feed)
            entries += feedparser.parse(r.text).entries
            print(feed)
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
            icons = [i for i in favicon.get(url) if i.format == 'png']
            print('---', '\n', url)
            if icons:
                icon = icons[0]
                print(icon.url)
                print(icon.format, icon.width, icon.height)
            else:
                print('missing')

    def handle(self, *args, **options):
        self.grab_entries()
        self.fetch()
