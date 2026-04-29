import pytest
from scraper.channel_reader import read_channels, extract_channel_name


def test_read_channels_basic(tmp_path):
    f = tmp_path / "channels.txt"
    f.write_text("https://t.me/s/habr_com\nhttps://t.me/s/prompt_design\nhttps://t.me/s/tired_glebmikheev\n")
    result = read_channels(str(f))
    assert result == [
        "https://t.me/s/habr_com",
        "https://t.me/s/prompt_design",
        "https://t.me/s/tired_glebmikheev",
    ]


def test_read_channels_skips_blank_lines(tmp_path):
    f = tmp_path / "channels.txt"
    f.write_text("https://t.me/s/habr_com\n\n\nhttps://t.me/s/prompt_design\n")
    result = read_channels(str(f))
    assert result == ["https://t.me/s/habr_com", "https://t.me/s/prompt_design"]


def test_read_channels_skips_comments(tmp_path):
    f = tmp_path / "channels.txt"
    f.write_text("# tech channels\nhttps://t.me/s/habr_com\n# another comment\nhttps://t.me/s/prompt_design\n")
    result = read_channels(str(f))
    assert result == ["https://t.me/s/habr_com", "https://t.me/s/prompt_design"]


def test_read_channels_strips_whitespace(tmp_path):
    f = tmp_path / "channels.txt"
    f.write_text("  https://t.me/s/habr_com  \n  https://t.me/s/prompt_design\n")
    result = read_channels(str(f))
    assert result == ["https://t.me/s/habr_com", "https://t.me/s/prompt_design"]


def test_read_channels_missing_file():
    with pytest.raises(FileNotFoundError):
        read_channels("/nonexistent/path/channels.txt")


def test_extract_channel_name_standard():
    assert extract_channel_name("https://t.me/s/habr_com") == "habr_com"


def test_extract_channel_name_trailing_slash():
    assert extract_channel_name("https://t.me/s/habr_com/") == "habr_com"


def test_extract_channel_name_invalid_url():
    with pytest.raises(ValueError):
        extract_channel_name("https://example.com/something")
