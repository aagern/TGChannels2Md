import os
from datetime import datetime, timezone
from scraper.writer import build_filename, write_markdown


START = datetime(2026, 4, 22, 0, 0, 0, tzinfo=timezone.utc)
END = datetime(2026, 4, 29, 0, 0, 0, tzinfo=timezone.utc)


def test_build_filename_format():
    name = build_filename("habr_com", START, END)
    assert name == "posts_habr_com_2026-04-22_2026-04-29.md"


def test_build_filename_special_chars():
    name = build_filename("tired_glebmikheev", START, END)
    assert name == "posts_tired_glebmikheev_2026-04-22_2026-04-29.md"


def test_write_markdown_creates_file(tmp_path):
    filepath = str(tmp_path / "output.md")
    write_markdown("# Hello", filepath)
    assert os.path.exists(filepath)
    with open(filepath, encoding="utf-8") as f:
        assert f.read() == "# Hello"


def test_write_markdown_creates_parent_dirs(tmp_path):
    filepath = str(tmp_path / "subdir" / "deep" / "output.md")
    write_markdown("content", filepath)
    assert os.path.exists(filepath)


def test_write_markdown_utf8(tmp_path):
    cyrillic = "# Привет мир\n\nКириллица работает."
    filepath = str(tmp_path / "cyrillic.md")
    write_markdown(cyrillic, filepath)
    with open(filepath, encoding="utf-8") as f:
        assert f.read() == cyrillic
