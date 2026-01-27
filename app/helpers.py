import urllib
import hashlib
from bs4 import BeautifulSoup


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def get_url(link):
    url = urllib.parse.urlparse(link)
    url_list = list(url)
    url_list[4] = ""
    return urllib.parse.urlunparse(url_list)


def get_description(entry):
    description = entry.get('description')
    if not description:
        description = entry.get('summary')
    if not description:
        description = ""
    soup = BeautifulSoup(description, features="lxml")
    lines = [l.strip() for l in soup.text.split('\n') if l.strip()]
    return lines[0]