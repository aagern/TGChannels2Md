import os
import pytest
from unittest.mock import patch
from scraper.cli import parse_args, main


def test_parse_args_required_days():
    args = parse_args(["--days", "7"])
    assert args.days == 7


def test_parse_args_defaults():
    args = parse_args(["--days", "3"])
    assert args.channels == "channels.txt"
    assert args.output_dir == "."
    assert args.delay == 1.0


def test_parse_args_custom_channels():
    args = parse_args(["--days", "5", "--channels", "mylist.txt"])
    assert args.channels == "mylist.txt"


def test_parse_args_missing_days():
    with pytest.raises(SystemExit):
        parse_args([])


def test_main_missing_channels_file(tmp_path):
    result = main(["--days", "3", "--channels", str(tmp_path / "nonexistent.txt"), "--output-dir", str(tmp_path)])
    assert result == 1


def test_main_end_to_end(tmp_path):
    channels_file = tmp_path / "channels.txt"
    channels_file.write_text("https://t.me/s/habr_com\n")

    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "sample_page.html")
    with open(fixture_path, encoding="utf-8") as f:
        fixture_html = f.read()

    with patch("scraper.cli.fetch_channel_pages", return_value=iter([fixture_html])):
        result = main([
            "--days", "30",
            "--channels", str(channels_file),
            "--output-dir", str(tmp_path),
        ])

    assert result == 0
    files = list(tmp_path.glob("posts_habr_com_*.md"))
    assert len(files) == 1
    content = files[0].read_text(encoding="utf-8")
    assert "habr_com" in content


def test_main_partial_failure(tmp_path):
    channels_file = tmp_path / "channels.txt"
    channels_file.write_text("https://t.me/s/habr_com\n")

    with patch("scraper.cli.fetch_channel_pages", side_effect=Exception("HTTP error")):
        result = main([
            "--days", "3",
            "--channels", str(channels_file),
            "--output-dir", str(tmp_path),
        ])

    assert result == 1
