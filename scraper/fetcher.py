import time
from datetime import datetime
from typing import Iterator
import requests
from scraper.parser import parse_posts, get_min_message_id


def fetch_page(url: str, session: requests.Session, delay: float = 1.0) -> str:
    time.sleep(delay)
    response = session.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text


def fetch_channel_pages(
    channel_url: str,
    since: datetime,
    session: requests.Session,
    delay: float = 1.0,
    max_pages: int = 50,
) -> Iterator[str]:
    url = channel_url
    for _ in range(max_pages):
        html = fetch_page(url, session, delay=delay)
        posts = parse_posts(html, "")
        if not posts:
            return
        yield html
        oldest = min(p.published_at for p in posts)
        if oldest <= since:
            return
        min_id = get_min_message_id(html)
        if min_id is None:
            return
        url = f"{channel_url}?before={min_id}"
