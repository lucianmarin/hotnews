import feedparser
import requests
import urllib

from datetime import datetime, timedelta
from helpers import feeds, load_db, save_db, to_date

token = "531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0"
api_path = "https://graph.facebook.com/v2.8/?id={0}&access_token={1}"
days_ago = (datetime.now() - timedelta(days=3)).timestamp()

data = load_db()

entries = []
for feed in feeds:
    response = requests.get(feed)
    entries += feedparser.parse(response.content).entries
    print(feed)

for entry in entries:
    if entry.link not in data:
        item = {
            'link': entry.link,
            'time': to_date(entry.published_parsed).timestamp(),
            'published': to_date(entry.published_parsed).isoformat(),
            'author': entry.get('author', ''),
            'title': entry.get('title', '')
        }
        if item['time'] > days_ago:
            data[entry.link] = item
        else:
            print(item['time'], item['link'])

allowed = True
values = sorted(data.values(), key=lambda k: k['time'], reverse=True)
filtered = {v['link'] for v in values if v['time'] > days_ago}

for key in filtered:
    if allowed:
        url = urllib.parse.quote(data[key]['link'])
        graph = api_path.format(url, token)
        if 'shares' not in data[key] or 'description' not in data[key]:
            facebook = requests.get(graph).json()
            if 'error' in facebook:
                allowed = False
            if 'share' in facebook:
                share = facebook['share']
                data[key]['shares'] = int(share.get('share_count', 0))
            if 'og_object' in facebook:
                og = facebook['og_object']
                data[key]['description'] = og.get('description', '')
            print(facebook)

print(len(data.keys()))

save_db(data)
