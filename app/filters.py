from urllib import parse
from datetime import datetime


def hostname(value):
    """Get hostname from an url."""
    url = parse.urlsplit(value)
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


def superscript(number):
    """Convert 1 to sup(1)."""
    text = str(number)
    text = text.replace('0', chr(8304))
    text = text.replace('1', chr(185))
    text = text.replace('2', chr(178))
    text = text.replace('3', chr(179))
    text = text.replace('4', chr(8308))
    text = text.replace('5', chr(8309))
    text = text.replace('6', chr(8310))
    text = text.replace('7', chr(8311))
    text = text.replace('8', chr(8312))
    text = text.replace('9', chr(8313))
    return text
