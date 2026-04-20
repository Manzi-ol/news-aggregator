"""
news-aggregator — Fetch top headlines from multiple RSS feeds
                  and display them in the terminal, with optional
                  saving to a daily digest text file.

No API key required — uses public RSS feeds.

Usage:
    python aggregator.py
    python aggregator.py --category tech
    python aggregator.py --save
    python aggregator.py --limit 5
"""

import argparse
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

RSS_FEEDS = {
    "world": [
        ("BBC World",    "http://feeds.bbci.co.uk/news/world/rss.xml"),
        ("Reuters",      "https://feeds.reuters.com/Reuters/worldNews"),
        ("Al Jazeera",   "https://www.aljazeera.com/xml/rss/all.xml"),
    ],
    "tech": [
        ("TechCrunch",   "https://techcrunch.com/feed/"),
        ("Ars Technica", "http://feeds.arstechnica.com/arstechnica/index"),
        ("The Verge",    "https://www.theverge.com/rss/index.xml"),
    ],
    "science": [
        ("NASA",         "https://www.nasa.gov/rss/dyn/breaking_news.rss"),
        ("ScienceDaily", "https://www.sciencedaily.com/rss/all.xml"),
    ],
    "business": [
        ("Financial Times",  "https://www.ft.com/rss/home/uk"),
        ("MarketWatch",      "http://feeds.marketwatch.com/marketwatch/topstories/"),
    ],
}


def fetch_feed(name: str, url: str, limit: int) -> list[dict]:
    try:
        req = Request(url, headers={"User-Agent": "NewsAggregator/1.0"})
        with urlopen(req, timeout=10) as resp:
            tree = ET.parse(resp)
    except (URLError, ET.ParseError) as e:
        print(f"  [!] Could not fetch {name}: {e}")
        return []

    items = []
    root = tree.getroot()
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    # Handle both RSS <item> and Atom <entry> formats
    entries = root.findall(".//item") or root.findall(".//atom:entry", ns)

    for entry in entries[:limit]:
        title_el = entry.find("title")
        link_el  = entry.find("link")
        date_el  = entry.find("pubDate") or entry.find("published") or entry.find("updated")

        title = title_el.text.strip() if title_el is not None and title_el.text else "No title"
        link  = (link_el.text or link_el.get("href", "")).strip() if link_el is not None else ""
        date  = date_el.text.strip()[:16] if date_el is not None and date_el.text else ""

        items.append({"source": name, "title": title, "link": link, "date": date})

    return items


def display(articles: list[dict]):
    if not articles:
        print("  No articles found.")
        return
    for i, a in enumerate(articles, 1):
        print(f"\n  {i:>3}. [{a['source']}]  {a['date']}")
        print(f"       {a['title']}")
        if a["link"]:
            print(f"       {a['link']}")


def save_digest(articles: list[dict]):
    os.makedirs("digests", exist_ok=True)
    path = f"digests/digest_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"News Digest — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        for a in articles:
            f.write(f"[{a['source']}] {a['date']}\n")
            f.write(f"{a['title']}\n")
            f.write(f"{a['link']}\n\n")
    print(f"\n  Digest saved to {path}\n")


def main():
    parser = argparse.ArgumentParser(description="RSS News Aggregator")
    parser.add_argument("--category", choices=list(RSS_FEEDS.keys()),
                        default="world", help="News category")
    parser.add_argument("--limit", type=int, default=5,
                        help="Max articles per source")
    parser.add_argument("--save", action="store_true",
                        help="Save digest to a text file")
    args = parser.parse_args()

    feeds = RSS_FEEDS[args.category]
    print(f"\n  Fetching {args.category.title()} news from {len(feeds)} sources …\n")

    all_articles: list[dict] = []
    for name, url in feeds:
        articles = fetch_feed(name, url, args.limit)
        all_articles.extend(articles)
        print(f"  ✓ {name}: {len(articles)} article(s)")

    display(all_articles)

    if args.save:
        save_digest(all_articles)


if __name__ == "__main__":
    main()
