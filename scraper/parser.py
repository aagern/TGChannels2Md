from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Tuple, Optional
from bs4 import BeautifulSoup


@dataclass
class Post:
    message_id: int
    channel: str
    published_at: datetime
    text: str
    links: List[Tuple[str, str]] = field(default_factory=list)


def parse_posts(html: str, channel: str) -> List[Post]:
    soup = BeautifulSoup(html, "lxml")
    posts = []
    for wrap in soup.select(".tgme_widget_message_wrap"):
        post_el = wrap.select_one("[data-post]")
        if post_el is None:
            continue
        time_el = wrap.select_one("time[datetime]")
        if time_el is None:
            continue
        raw_dt = time_el.get("datetime")
        dt = datetime.fromisoformat(raw_dt).astimezone(timezone.utc)
        msg_id = int(post_el.get("data-post").split("/")[-1])
        text_el = wrap.select_one(".tgme_widget_message_text")
        text = text_el.get_text(separator="\n").strip() if text_el else ""
        links = extract_links(text_el) if text_el else []
        posts.append(Post(message_id=msg_id, channel=channel, published_at=dt, text=text, links=links))
    return sorted(posts, key=lambda p: p.published_at)


def extract_links(tag) -> List[Tuple[str, str]]:
    seen_urls = set()
    result = []
    for a in tag.select("a[href]"):
        url = a.get("href", "")
        if not url or not url.startswith("http"):
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        anchor = a.get_text(strip=True) or url
        result.append((anchor, url))
    return result


def get_min_message_id(html: str) -> Optional[int]:
    soup = BeautifulSoup(html, "lxml")
    ids = []
    for el in soup.select("[data-post]"):
        raw = el.get("data-post", "")
        parts = raw.split("/")
        if len(parts) == 2 and parts[1].isdigit():
            ids.append(int(parts[1]))
    return min(ids) if ids else None
