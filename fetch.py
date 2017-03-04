import datetime
import feedparser
import json
import requests
import urllib

from config import feeds
from werkzeug.contrib.cache import FileSystemCache

cache = FileSystemCache('/Volumes/GitHub/subfeeder/cache')
total = 0


def to_date(s):
    return datetime.datetime(s.tm_year, s.tm_mon, s.tm_mday, s.tm_hour, s.tm_min, s.tm_sec, tzinfo=datetime.timezone.utc)


for feed in feeds:
    print('Fetching {0}'.format(feed))
    start = datetime.datetime.utcnow()
    response = requests.get(feed)
    entries = feedparser.parse(response.content).entries
    items = []
    for entry in entries:
        item = {}
        if entry.id.startswith('https://www.neowin.net/'):
            item['link'] = entry.id
        else:
            item['link'] = entry.link
        token = '531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0'
        url = urllib.parse.quote(item['link'])
        graph = 'https://graph.facebook.com/v2.7/?id={0}&access_token={1}'.format(url, token)
        facebook = json.loads(requests.get(graph).text)
        item['shares'] = 0
        item['description'] = ''
        try:
            item['shares'] = facebook['share']['share_count']
        except:
            pass
        try:
            item['description'] = facebook['og_object']['description']
        except:
            pass
        item['time'] = to_date(entry.published_parsed).timestamp()
        item['published'] = to_date(entry.published_parsed).isoformat()
        item['author'] = entry.get('author', '')
        item['title'] = entry.get('title', '')
        items.append(item)
    end = datetime.datetime.utcnow()
    current = (end - start).total_seconds()
    total += current
    print('Time {0} seconds'.format(current))
    cache.set(feed, items, timeout=0)


print('Total {0} minutes'.format(round(total/60, 2)))
