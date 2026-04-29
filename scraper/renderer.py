from datetime import datetime
from typing import List
from itertools import groupby
from scraper.parser import Post


def render_channel_markdown(
    channel_name: str,
    channel_url: str,
    posts: List[Post],
    start: datetime,
    end: datetime,
) -> str:
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    lines = [
        f"# Posts from @{channel_name} | {start_str} – {end_str}",
        "",
        f"Source: {channel_url}",
        "",
        "---",
        "",
    ]
    if not posts:
        lines.append(f"*No posts found in this period ({start_str} – {end_str}).*")
        return "\n".join(lines)

    sorted_posts = sorted(posts, key=lambda p: p.published_at)
    for date_key, group in groupby(sorted_posts, key=lambda p: p.published_at.date()):
        lines.append(f"## {date_key}")
        lines.append("")
        for post in group:
            lines.append(format_post(post))
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def format_post(post: Post) -> str:
    time_str = post.published_at.strftime("%H:%M")
    post_url = f"https://t.me/{post.channel}/{post.message_id}"
    lines = [
        f"**[Post {post.message_id}]({post_url})** — {time_str}",
        "",
        post.text,
    ]
    if post.links:
        lines.append("")
        lines.append("**Links:**")
        for anchor, url in post.links:
            lines.append(f"- [{anchor}]({url})")
    return "\n".join(lines)
