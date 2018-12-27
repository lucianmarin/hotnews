import urllib
from datetime import datetime


def hostname(value):
    """Get hostname from an url."""
    url = urllib.parse.urlsplit(value)
    return url.netloc.replace('www.', '')


def sitename(value):
    """Get sitename without LTD part."""
    parts = value.split('.')
    parts.reverse()
    del parts[0]
    parts.reverse()
    return ".".join(parts)


def date(stamp):
    """Format date time."""
    timestamp = datetime.fromtimestamp(stamp)
    return timestamp.strftime('%b %-e, %Y %H:%M')


def shortdate(stamp):
    """Short time interval for a timestamp."""
    timestamp = datetime.utcfromtimestamp(stamp)
    delta = datetime.utcnow() - timestamp
    minutes = round(delta.total_seconds() / 60)
    hours = round(delta.total_seconds() / 3600)
    if minutes < 60:
        return "{0}m".format(minutes)
    return "{0}h".format(hours)
