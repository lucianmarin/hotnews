from datetime import datetime, timezone

import tldextract


def hostname(value):
    """Get hostname from an url."""
    r = tldextract.extract(value)
    if r.subdomain in ['', 'www']:
        return f'{r.domain}.{r.suffix}'
    return f'{r.subdomain}.{r.domain}.{r.suffix}'


def sitename(value):
    """Get sitename without TLD part."""
    r = tldextract.extract(value)
    if r.subdomain in ['', 'www']:
        return f'{r.domain}'
    return f'{r.subdomain}.{r.domain}'


def date(stamp):
    """Format date time."""
    timestamp = datetime.fromtimestamp(stamp)
    return timestamp.strftime('%b %-e, %Y %H:%M')


def shortdate(timestamp):
    """Short time interval for a timestamp."""
    total_seconds = datetime.now(timezone.utc).timestamp() - timestamp
    minutes = round(total_seconds / 60)
    hours = round(total_seconds / 3600)
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
    return text.replace('9', chr(8313))
