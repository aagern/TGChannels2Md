from datetime import datetime, timezone, timedelta
from scraper.filters import filter_by_date_window, compute_date_window
from scraper.parser import Post


def make_post(channel, message_id, dt_str):
    dt = datetime.fromisoformat(dt_str)
    return Post(message_id=message_id, channel=channel, published_at=dt, text="text", links=[])


START = datetime(2026, 4, 26, 0, 0, 0, tzinfo=timezone.utc)
END = datetime(2026, 4, 29, 23, 59, 59, tzinfo=timezone.utc)


def test_filter_by_date_window_all_in():
    posts = [
        make_post("ch", 1, "2026-04-26T12:00:00+00:00"),
        make_post("ch", 2, "2026-04-28T08:00:00+00:00"),
    ]
    result = filter_by_date_window(posts, START, END)
    assert len(result) == 2


def test_filter_by_date_window_some_out():
    posts = [
        make_post("ch", 1, "2026-04-25T23:59:59+00:00"),  # before start
        make_post("ch", 2, "2026-04-27T10:00:00+00:00"),  # in window
        make_post("ch", 3, "2026-04-30T00:00:01+00:00"),  # after end
    ]
    result = filter_by_date_window(posts, START, END)
    assert len(result) == 1
    assert result[0].message_id == 2


def test_filter_by_date_window_inclusive_bounds():
    posts = [
        make_post("ch", 1, "2026-04-26T00:00:00+00:00"),  # exactly start
        make_post("ch", 2, "2026-04-29T23:59:59+00:00"),  # exactly end
    ]
    result = filter_by_date_window(posts, START, END)
    assert len(result) == 2


def test_filter_by_date_window_empty_input():
    result = filter_by_date_window([], START, END)
    assert result == []


def test_compute_date_window_days_back():
    ref = datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc)
    start, end = compute_date_window(3, reference=ref)
    assert end == ref
    assert start == ref - timedelta(days=3)


def test_compute_date_window_utc_aware():
    start, end = compute_date_window(7)
    assert start.tzinfo is not None
    assert end.tzinfo is not None
    assert start.tzinfo == timezone.utc
    assert end.tzinfo == timezone.utc


def test_compute_date_window_custom_reference():
    ref = datetime(2026, 1, 10, 0, 0, 0, tzinfo=timezone.utc)
    start, end = compute_date_window(5, reference=ref)
    assert end == ref
    assert start == datetime(2026, 1, 5, 0, 0, 0, tzinfo=timezone.utc)
