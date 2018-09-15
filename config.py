from werkzeug.contrib.cache import FileSystemCache

cache = FileSystemCache('./cache')

feeds = ['http://feeds.arstechnica.com/arstechnica/index/',
         'http://feeds.macrumors.com/MacRumors-Front',
         'http://feeds.feedburner.com/d0od',
         # 'http://feeds.feedburner.com/neowin-main',
         'http://feeds.feedburner.com/sub/9to5mac',
         'http://feeds.feedburner.com/sub/anandtech',
         'http://feeds.feedburner.com/sub/engadget',
         'http://feeds.feedburner.com/sub/gsmarena',
         'http://feeds.feedburner.com/sub/nautilus',
         'http://feeds.feedburner.com/sub/recode',
         'http://feeds.feedburner.com/sub/techcrunch',
         'http://feeds.feedburner.com/sub/verge',
         'https://news.ycombinator.com/rss',
         'https://lobste.rs/rss']

ro_feeds = ['http://feeds.feedburner.com/hotnews/yvoq',
         'http://feeds.feedburner.com/sub/stiripesurse',
         'http://feeds.feedburner.com/sub/digi24']

new_feeds = ['http://qz.com/feed/',
   'http://www.digi24.ro/rss']
