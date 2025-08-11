# insert_finviz_headlines_windows.py
"""
Windows-friendly Finviz ingestor (authentic only).
- Fetches real headlines from Finviz
- Extracts ticker, headline, and published datetime
- Inserts only complete rows into MySQL (no seeding/fakes)
"""

from __future__ import annotations
import os, sys, traceback, re
from datetime import datetime
from typing import List, Dict, Optional

import mysql.connector

# Configuration (env-first; easy to override)
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "stock_news")

# If you want to enforce market hours later, set ENFORCE_MARKET_HOURS=1 in your env.
ENFORCE_MARKET_HOURS = os.getenv("ENFORCE_MARKET_HOURS", "0") == "1"

# Finviz news page (v=3 is the “compact” view)
FINVIZ_NEWS_URL = "https://finviz.com/news.ashx?v=3"


#  Small helpers def
def die(msg: str, e: Optional[BaseException] = None) -> None:
    """Print a clear reason and exit with failure."""
    print("FATAL:", msg)
    if e:
        print("DETAIL:", repr(e))
        traceback.print_exc()
    sys.exit(1)


def connect_db():
    """Open a short-timeout MySQL connection, or fail loudly."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            connection_timeout=5,
        )
        return conn, conn.cursor()
    except Exception as e:
        die("DB connection failed", e)


def parse_dt(text: str, carry_date: Optional[datetime.date]) -> Optional[datetime]:
    
    text = (text or "").strip()
    if not text:
        return None

    # Full stamp for time
    m_full = re.match(r"([A-Za-z]{3}-\d{2}-\d{2})\s+(\d{1,2}:\d{2}(AM|PM))", text)
    if m_full:
        try:
            return datetime.strptime(m_full.group(0), "%b-%d-%y %I:%M%p")
        except ValueError:
            return None

    # Time-only like '09:40AM' -> use carry_date
    m_time = re.match(r"(\d{1,2}:\d{2}(AM|PM))", text)
    if m_time and carry_date:
        try:
            t = datetime.strptime(m_time.group(1), "%I:%M%p").time()
            return datetime.combine(carry_date, t)
        except ValueError:
            return None

    return None


# Fetchers (pyfinviz first, then HTML fallback) 
def fetch_with_pyfinviz() -> List[Dict]:
    """
    Try pyfinviz if available. Returns list of dicts with keys:
    - ticker, headline, date
    """
    try:
        from pyfinviz.news import WebScraper  # type: ignore
    except Exception:
        return []

    try:
        ws = WebScraper()
        items = []
        # pyfinviz versions expose .news() or .latest() — try both
        for method in ("news", "latest"):
            if hasattr(ws, method):
                raw = getattr(ws, method)()
                if not raw:
                    continue
                for it in raw:
                    # Normalize across object/dict varieties
                    t = getattr(it, "ticker", None) or (it.get("ticker") if isinstance(it, dict) else None)
                    h = getattr(it, "title",  None) or (it.get("title")  if isinstance(it, dict) else None)
                    d = getattr(it, "date",   None) or (it.get("date")   if isinstance(it, dict) else None)
                    # Attempt to parse date strings if provided
                    if isinstance(d, str):
                        # pyfinviz sometimes provides '%Y-%m-%d %H:%M' or similar
                        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%b-%d-%y %I:%M%p"):
                            try:
                                d = datetime.strptime(d, fmt)
                                break
                            except Exception:
                                pass
                    # Keep only complete rows
                    if t and h and isinstance(d, datetime):
                        items.append({"ticker": t.strip(), "headline": h.strip(), "date": d})
        return items
    except Exception as e:
        print("pyfinviz fetch failed:", repr(e))
        return []


def fetch_with_html() -> List[Dict]:
    """
    Robust HTML parse against Finviz compact news.
      - Request with cloudscraper (handles common anti-bot)
      - Parse table rows; each news row has two tds: [date/time] [link/headline + small ticker link]
      - Extract date/time cell; carry the date forward when only time appears
      - Extract headline text from first <a>
      - Extract ticker from a 'quote.ashx?t=XYZ' link present in the row
    """
    try:
        import cloudscraper
        from bs4 import BeautifulSoup
        from urllib.parse import urlparse, parse_qs
    except Exception as e:
        print("Missing parser deps (install: cloudscraper beautifulsoup4):", repr(e))
        return []

    s = cloudscraper.create_scraper()
    H = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://finviz.com/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    r = s.get(FINVIZ_NEWS_URL, headers=H)
    if r.status_code != 200 or len(r.text) < 2000:
        print(f"HTTP not OK: {r.status_code}, len={len(r.text)}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    # Finviz news table
    rows = soup.select("table.fullview-news-outer tr")
    if not rows:  # layout variant fallback
        rows = soup.select("tr")

    items: List[Dict] = []
    carry_date: Optional[datetime.date] = None

    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 2:
            continue

        # First td: date/time (sometimes full stamp, sometimes just time)
        dt_text = tds[0].get_text(strip=True)
        dt = parse_dt(dt_text, carry_date)

        # Second td: contains links; first <a> is the headline
        a_headline = tds[1].find("a")
        headline = a_headline.get_text(strip=True) if a_headline else None

        # Find a link with 'quote.ashx?t=XYZ' to get the ticker
        ticker = None
        for a in tds[1].find_all("a", href=True):
            href = a["href"]
            if "quote.ashx" in href and "t=" in href:
                # Extract ticker from query param
                q = parse_qs(urlparse(href).query)
                tick_param = q.get("t") or q.get("T")  # be forgiving
                if tick_param and tick_param[0]:
                    ticker = tick_param[0].strip().upper()
                    break

        # Maintain carry_date whenever we see a full date
        if dt and dt_text and "-" in dt_text:
            carry_date = dt.date()

        # Keep only complete, authentic rows
        if ticker and headline and dt:
            items.append({"ticker": ticker, "headline": headline, "date": dt})

    return items


def main() -> None:
    print(">>> START insert_finviz_headlines_windows.py")

    if ENFORCE_MARKET_HOURS:
        now = datetime.now()
        if (now.weekday() >= 5) or (now.hour < 9) or (now.hour > 16) or (now.hour == 16 and now.minute > 30):
            print("Skipped: outside market hours")
            sys.exit(0)

    # 1) Try pyfinviz (cleanest); fall back to direct HTML parse
    items = fetch_with_pyfinviz() or fetch_with_html()
    print("parsed items:", len(items))

    if not items:
        print("No headlines parsed. Exiting without inserts (authentic-only).")
        sys.exit(0)

    conn, cur = connect_db()
    inserted = 0

    for it in items:
        t = (it.get("ticker") or "").strip()
        h = (it.get("headline") or "").strip()
        d = it.get("date")
        if not t or not h or not isinstance(d, datetime):
            # Authentic-only: skip incomplete rows
            print("[skip] incomplete:", it)
            continue

        cur.execute(
            "INSERT INTO headlines (ticker, headline, date) VALUES (%s, %s, %s)",
            (t, h, d),
        )
        inserted += 1

    conn.commit()
    conn.close()
    print("Inserted:", inserted)


if __name__ == "__main__":
    main()
