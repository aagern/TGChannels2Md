from datetime import datetime, timezone, timedelta
from typing import List, Tuple
from scraper.parser import Post


def filter_by_date_window(posts: List[Post], start: datetime, end: datetime) -> List[Post]:
    return [p for p in posts if start <= p.published_at <= end]


def compute_date_window(days_back: int, reference: datetime = None) -> Tuple[datetime, datetime]:
    end = reference if reference is not None else datetime.now(timezone.utc)
    start = end - timedelta(days=days_back)
    return start, end
