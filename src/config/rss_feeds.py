import feedparser

RSS_FEEDS = {
    "national_security": [
        "http://feeds.reuters.com/Reuters/worldNews",
        "http://feeds.bbci.co.uk/news/world/rss.xml"
    ],
    "domestic_affairs": [
        "https://www.npr.org/rss/rss.php?id=1014",
        "https://www.apnews.com/APTopHeadlines"
    ],
    "international_relations": [
        "https://news.un.org/feed/subscribe/en/news/all/rss.xml"
    ]
}

def fetch_rss_feed(url):
    """Fetch and parse an RSS feed."""
    feed = feedparser.parse(url)
    return feed["entries"][:3]
