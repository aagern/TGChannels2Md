import os
import pytest
from datetime import timezone
from scraper.parser import parse_posts, extract_links, get_min_message_id
from bs4 import BeautifulSoup

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "sample_page.html")


@pytest.fixture
def fixture_html():
    with open(FIXTURE_PATH, encoding="utf-8") as f:
        return f.read()


def test_parse_posts_count(fixture_html):
    posts = parse_posts(fixture_html, "habr_com")
    assert len(posts) == 20


def test_parse_posts_message_id(fixture_html):
    posts = parse_posts(fixture_html, "habr_com")
    assert posts[0].message_id == 68497


def test_parse_posts_channel(fixture_html):
    posts = parse_posts(fixture_html, "habr_com")
    assert all(p.channel == "habr_com" for p in posts)


def test_parse_posts_datetime_utc(fixture_html):
    posts = parse_posts(fixture_html, "habr_com")
    post = posts[0]
    assert post.published_at.tzinfo is not None
    assert post.published_at.tzinfo == timezone.utc
    assert post.published_at.year == 2026
    assert post.published_at.month == 4
    assert post.published_at.day == 28


def test_parse_posts_text_content(fixture_html):
    posts = parse_posts(fixture_html, "habr_com")
    assert len(posts[0].text) > 0
    assert "завод" in posts[0].text


def test_parse_posts_links_extracted(fixture_html):
    posts = parse_posts(fixture_html, "habr_com")
    assert len(posts[0].links) > 0
    texts, urls = zip(*posts[0].links)
    assert any("habr" in url or "u.habr" in url for url in urls)


def test_parse_posts_empty_page():
    posts = parse_posts("<html><body></body></html>", "habr_com")
    assert posts == []


def test_parse_posts_skips_no_datetime():
    html = """
    <html><body>
    <div class="tgme_widget_message_wrap">
      <div data-post="habr_com/1">
        <div class="tgme_widget_message_text">text without time</div>
      </div>
    </div>
    </body></html>
    """
    posts = parse_posts(html, "habr_com")
    assert posts == []


def test_extract_links_deduplication():
    html = '<div><a href="https://example.com">link1</a> and <a href="https://example.com">link2</a></div>'
    tag = BeautifulSoup(html, "lxml").find("div")
    links = extract_links(tag)
    urls = [url for _, url in links]
    assert urls.count("https://example.com") == 1


def test_extract_links_filters_relative_urls():
    html = '<div><a href="?q=test">hashtag</a><a href="https://example.com">real</a></div>'
    tag = BeautifulSoup(html, "lxml").find("div")
    links = extract_links(tag)
    urls = [url for _, url in links]
    assert "?q=test" not in urls
    assert "https://example.com" in urls


def test_get_min_message_id(fixture_html):
    min_id = get_min_message_id(fixture_html)
    assert min_id == 68497


def test_get_min_message_id_empty_page():
    result = get_min_message_id("<html><body></body></html>")
    assert result is None
