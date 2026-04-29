import argparse
import os
import sys
import requests
from typing import List, Optional
from scraper.channel_reader import read_channels, extract_channel_name
from scraper.fetcher import fetch_channel_pages
from scraper.filters import compute_date_window, filter_by_date_window
from scraper.parser import parse_posts
from scraper.renderer import render_channel_markdown
from scraper.writer import build_filename, write_markdown


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape public Telegram channels and save posts as Markdown.")
    parser.add_argument("--days", type=int, required=True, help="Number of days to look back")
    parser.add_argument("--channels", default="channels.txt", help="Path to channels list file (default: channels.txt)")
    parser.add_argument("--output-dir", default=".", help="Directory to write output files (default: .)")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between HTTP requests (default: 1.0)")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        urls = read_channels(args.channels)
    except FileNotFoundError:
        print(f"Error: channels file not found: {args.channels}", file=sys.stderr)
        return 1

    start, end = compute_date_window(args.days)
    session = requests.Session()
    exit_code = 0

    for url in urls:
        try:
            channel_name = extract_channel_name(url)
        except ValueError as e:
            print(f"Warning: skipping invalid URL {url}: {e}", file=sys.stderr)
            exit_code = 1
            continue
        try:
            all_posts = []
            for html in fetch_channel_pages(url, since=start, session=session, delay=args.delay):
                all_posts.extend(parse_posts(html, channel_name))
            posts = filter_by_date_window(all_posts, start, end)
            content = render_channel_markdown(channel_name, url, posts, start, end)
            filename = build_filename(channel_name, start, end)
            filepath = os.path.join(args.output_dir, filename)
            write_markdown(content, filepath)
            print(f"Saved {len(posts)} posts -> {filepath}")
        except Exception as e:
            print(f"Error scraping {url}: {e}", file=sys.stderr)
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
