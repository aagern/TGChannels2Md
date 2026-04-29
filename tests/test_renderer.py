from datetime import datetime, timezone
from scraper.renderer import render_channel_markdown, format_post
from scraper.parser import Post


def make_post(message_id, dt_str, text, links=None):
    dt = datetime.fromisoformat(dt_str)
    return Post(message_id=message_id, channel="habr_com", published_at=dt, text=text, links=links or [])


START = datetime(2026, 4, 26, 0, 0, 0, tzinfo=timezone.utc)
END = datetime(2026, 4, 29, 0, 0, 0, tzinfo=timezone.utc)
CHANNEL_URL = "https://t.me/s/habr_com"


def test_render_channel_markdown_header():
    posts = [make_post(1, "2026-04-27T10:00:00+00:00", "Hello")]
    md = render_channel_markdown("habr_com", CHANNEL_URL, posts, START, END)
    assert "habr_com" in md
    assert "2026-04-26" in md
    assert "2026-04-29" in md


def test_render_channel_markdown_date_groups():
    posts = [
        make_post(1, "2026-04-26T10:00:00+00:00", "Post one"),
        make_post(2, "2026-04-27T10:00:00+00:00", "Post two"),
    ]
    md = render_channel_markdown("habr_com", CHANNEL_URL, posts, START, END)
    assert "## 2026-04-26" in md
    assert "## 2026-04-27" in md


def test_render_channel_markdown_post_text():
    posts = [make_post(1, "2026-04-27T10:00:00+00:00", "Unique post content here")]
    md = render_channel_markdown("habr_com", CHANNEL_URL, posts, START, END)
    assert "Unique post content here" in md


def test_render_channel_markdown_links_preserved():
    posts = [make_post(1, "2026-04-27T10:00:00+00:00", "See article", [("Read more", "https://habr.com/article")])]
    md = render_channel_markdown("habr_com", CHANNEL_URL, posts, START, END)
    assert "https://habr.com/article" in md


def test_render_channel_markdown_post_url():
    posts = [make_post(68497, "2026-04-27T10:00:00+00:00", "Some post")]
    md = render_channel_markdown("habr_com", CHANNEL_URL, posts, START, END)
    assert "https://t.me/habr_com/68497" in md


def test_render_channel_markdown_empty_posts():
    md = render_channel_markdown("habr_com", CHANNEL_URL, [], START, END)
    assert "no posts" in md.lower() or "0" in md


def test_render_channel_markdown_ordering():
    posts = [
        make_post(2, "2026-04-27T15:00:00+00:00", "Second"),
        make_post(1, "2026-04-27T08:00:00+00:00", "First"),
    ]
    md = render_channel_markdown("habr_com", CHANNEL_URL, posts, START, END)
    assert md.index("First") < md.index("Second")


def test_format_post_no_links():
    post = make_post(1, "2026-04-27T10:00:00+00:00", "Plain text, no links")
    result = format_post(post)
    assert "Plain text, no links" in result
    assert "Links:" not in result
