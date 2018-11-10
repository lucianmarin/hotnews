from datetime import datetime, timezone


feeds = ['http://feeds.feedburner.com/sub/daringfireball',
         'http://feeds.arstechnica.com/arstechnica/index/',
         'http://feeds.macrumors.com/MacRumors-Front',
         'http://feeds.feedburner.com/sub/9to5google',
         'http://feeds.feedburner.com/sub/9to5mac',
         'http://feeds.feedburner.com/sub/anandtech',
         'http://feeds.feedburner.com/sub/electrek',
         'http://feeds.feedburner.com/sub/engadget',
         'http://feeds.feedburner.com/sub/gsmarena',
         'http://feeds.feedburner.com/sub/nautilus',
         'http://feeds.feedburner.com/sub/techcrunch',
         'http://feeds.feedburner.com/sub/verge',
         'https://news.ycombinator.com/rss',
         'https://lobste.rs/rss']


def to_date(s):
    return datetime(s.tm_year, s.tm_mon, s.tm_mday,
                    s.tm_hour, s.tm_min, s.tm_sec, tzinfo=timezone.utc)
