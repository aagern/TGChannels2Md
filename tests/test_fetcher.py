import os
import pytest
import responses as responses_lib
import requests
from datetime import datetime, timezone
from unittest.mock import patch
from scraper.fetcher import fetch_page, fetch_channel_pages

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "sample_page.html")

with open(FIXTURE_PATH, encoding="utf-8") as _f:
    FIXTURE_HTML = _f.read()

# A minimal HTML page with one old post (before any test window)
OLD_POST_HTML = """
<html><body>
<div class="tgme_widget_message_wrap">
  <div data-post="habr_com/100">
    <time datetime="2020-01-01T00:00:00+00:00"></time>
    <div class="tgme_widget_message_text">old post</div>
  </div>
</div>
</body></html>
"""


@responses_lib.activate
def test_fetch_page_success():
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body=FIXTURE_HTML, status=200)
    session = requests.Session()
    html = fetch_page("https://t.me/s/habr_com", session, delay=0)
    assert "tgme_widget_message" in html


@responses_lib.activate
def test_fetch_page_applies_delay():
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body="ok", status=200)
    session = requests.Session()
    with patch("time.sleep") as mock_sleep:
        fetch_page("https://t.me/s/habr_com", session, delay=1.5)
        mock_sleep.assert_called_once_with(1.5)


@responses_lib.activate
def test_fetch_page_raises_on_404():
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body="Not Found", status=404)
    session = requests.Session()
    with pytest.raises(requests.HTTPError):
        fetch_page("https://t.me/s/habr_com", session, delay=0)


@responses_lib.activate
def test_fetch_page_raises_on_429():
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body="Rate Limited", status=429)
    session = requests.Session()
    with pytest.raises(requests.HTTPError):
        fetch_page("https://t.me/s/habr_com", session, delay=0)


@responses_lib.activate
def test_fetch_channel_pages_single_page():
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body=FIXTURE_HTML, status=200)
    since = datetime(2026, 4, 27, 0, 0, 0, tzinfo=timezone.utc)
    session = requests.Session()
    pages = list(fetch_channel_pages("https://t.me/s/habr_com", since, session, delay=0))
    assert len(pages) >= 1
    assert "tgme_widget_message" in pages[0]


@responses_lib.activate
def test_fetch_channel_pages_stops_at_since():
    # Fixture has posts from 2026-04-28 onwards; since=2020-01-01 means we stop after first page
    # because oldest post (2026-04-28) is still newer... wait, that means we'd paginate.
    # Let's set since to something recent so all posts are after it and we stop.
    # The fixture oldest post is 2026-04-28T07:02:19; set since to 2026-04-28 -> should stop
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body=FIXTURE_HTML, status=200)
    # Second pagination request with ?before=68497 returns an old page
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body=OLD_POST_HTML, status=200)
    since = datetime(2026, 4, 20, 0, 0, 0, tzinfo=timezone.utc)
    session = requests.Session()
    pages = list(fetch_channel_pages("https://t.me/s/habr_com", since, session, delay=0))
    # Should have fetched 2 pages (first + paginated-back-in-time page)
    assert len(pages) == 2


@responses_lib.activate
def test_fetch_channel_pages_max_pages_cap():
    # Always return the fixture (posts always newer than since) — should stop at max_pages
    for _ in range(10):
        responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body=FIXTURE_HTML, status=200)
    since = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    session = requests.Session()
    pages = list(fetch_channel_pages("https://t.me/s/habr_com", since, session, delay=0, max_pages=3))
    assert len(pages) == 3


@responses_lib.activate
def test_fetch_channel_pages_empty_channel():
    empty_html = "<html><body></body></html>"
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body=empty_html, status=200)
    since = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
    session = requests.Session()
    pages = list(fetch_channel_pages("https://t.me/s/habr_com", since, session, delay=0))
    assert pages == []


@responses_lib.activate
def test_fetch_channel_pages_pagination():
    # First page has min_id=68497. Second request should include ?before=68497
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body=FIXTURE_HTML, status=200)
    responses_lib.add(responses_lib.GET, "https://t.me/s/habr_com", body=OLD_POST_HTML, status=200)
    since = datetime(2026, 4, 20, 0, 0, 0, tzinfo=timezone.utc)
    session = requests.Session()
    list(fetch_channel_pages("https://t.me/s/habr_com", since, session, delay=0))
    # Second call URL should have ?before=68497
    assert "before=68497" in responses_lib.calls[1].request.url
