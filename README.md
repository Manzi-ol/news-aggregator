# News Aggregator

> Fetch top headlines from multiple RSS sources in your terminal — **no API key required**.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![RSS](https://img.shields.io/badge/RSS-FFA500?style=flat&logo=rss&logoColor=white)

---

## Preview

```
  Fetching World news from 3 sources …

  ✓ BBC World: 5 article(s)
  ✓ Reuters: 5 article(s)
  ✓ Al Jazeera: 5 article(s)

    1. [BBC World]  Mon 20 Apr
       African Union summit opens in Addis Ababa
       https://feeds.bbci.co.uk/...

    2. [Reuters]  Mon 20 Apr
       Global markets steady ahead of Fed decision
       https://feeds.reuters.com/...
```

---

## Install & Run

```bash
git clone https://github.com/Manzi-ol/news-aggregator
cd news-aggregator
# No pip install needed — standard library only
python aggregator.py
```

---

## Usage

```bash
python aggregator.py                      # World news (default)
python aggregator.py --category tech      # Tech headlines
python aggregator.py --category science   # Science news
python aggregator.py --category business  # Business news
python aggregator.py --limit 10           # 10 articles per source
python aggregator.py --save               # Save to daily digest file
```

---

## Sources

| Category | Sources |
|----------|---------|
| `world` | BBC World, Reuters, Al Jazeera |
| `tech` | TechCrunch, Ars Technica, The Verge |
| `science` | NASA, ScienceDaily |
| `business` | Financial Times, MarketWatch |

---

## Zero Dependencies

Uses Python standard library only — `xml.etree`, `urllib`, `csv`. No pip install needed.

---

*Part of [Manzi's 100 GitHub Projects Roadmap](https://github.com/Manzi-ol) · Project #21*