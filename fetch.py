import feedparser
import requests
import urllib
import time

from helpers import feeds, to_date
from models import News

token = "531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0"
api_path = "https://graph.facebook.com/v2.8/?id={0}&access_token={1}"
is_allowed = False

entries = []
for feed in feeds:
    response = requests.get(feed)
    entries += feedparser.parse(response.content).entries
    print(feed)

for entry in entries:
    try:
        n = News(link=entry.link, title=entry.title)
        n.time = to_date(entry.published_parsed).timestamp()
        n.author = entry.get('author', None)
        n.save()
    except Exception as e:
        print(e)

# clean up
News.query.filter(time=(None, time.time() - 48 * 3600)).delete()

for entry in News.query.filter(time=(time.time() - 8 * 3600, None)):
    if is_allowed and entry.description is None:
        url = urllib.parse.quote(entry.link)
        graph = api_path.format(url, token)
        fb = requests.get(graph).json()
        if 'error' in fb:
            is_allowed = False
            print('error')
        else:
            og_object = fb.get('og_object', {})
            entry.description = og_object.get('description', '')
            entry.save()
            print(entry.description)


for entry in News.query.filter(time=(None, time.time() - 8 * 3600)):
    if is_allowed and entry.shares is None:
        url = urllib.parse.quote(entry.link)
        graph = api_path.format(url, token)
        fb = requests.get(graph).json()
        if 'error' in fb:
            is_allowed = False
            print('error')
        else:
            og_object = fb.get('og_object', {})
            entry.description = og_object.get('description', '')
            share = fb.get('share', {})
            entry.shares = share.get('share_count', 0)
            entry.save()
            print(entry.shares)
