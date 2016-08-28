import json
import urllib
from config import feeds
from datetime import datetime
from time import mktime

import feedparser
import requests
from werkzeug.contrib.cache import MemcachedCache

cache = MemcachedCache(['127.0.0.1:11211'])
total = 0


for feed in feeds:
    print('Fetching', feed)
    start = datetime.utcnow()
    response = requests.get(feed)
    items = feedparser.parse(response.content).entries
    for item in items:
        redirect = requests.head(item.link, allow_redirects=True)
        item['link'] = urllib.parse.urljoin(redirect.url, urllib.parse.urlparse(redirect.url).path)
        item['elapsed'] = redirect.elapsed.total_seconds()
        graph = 'https://graph.facebook.com/v2.7/?id=' + urllib.parse.quote(item.link) + '&access_token=531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0'
        facebook = requests.get(graph)
        item['facebook'] = json.loads(facebook.text)
        if not 'share' in item['facebook']:
            item['facebook']['share'] = {}
            item['facebook']['share']['share_count'] = 0
        item['timed'] = mktime(item.published_parsed)
    end = datetime.utcnow()
    total += (end - start).total_seconds()
    print('Time', (end - start).seconds, 'seconds')
    cache.set(feed, items, timeout=3600)

print('Total', round(total/60, 2), 'minutes')
