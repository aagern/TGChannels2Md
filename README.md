# TGChannels Scraper

Scrapes public Telegram channels and saves posts from a given time window as Markdown files.

Works with any channel accessible at `https://t.me/s/<channel>` — no API key required.

## Requirements

Python 3.9+ and the dependencies in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Setup

Create `channels.txt` with one channel URL per line:

```
https://t.me/s/habr_com
https://t.me/s/prompt_design
# comments and blank lines are ignored
```

## Usage

```bash
python -m scraper.cli --days <N> [options]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--days N` | *(required)* | Number of days to look back from now |
| `--channels FILE` | `channels.txt` | Path to the channels list file |
| `--output-dir DIR` | `.` (current dir) | Directory to write output Markdown files |
| `--delay FLOAT` | `1.0` | Seconds to wait between HTTP requests |

### Examples

```bash
# Scrape last 3 days from channels.txt into current directory
python -m scraper.cli --days 3

# Scrape last 7 days, custom channels file, save to ./output/
python -m scraper.cli --days 7 --channels my_channels.txt --output-dir ./output

# Reduce delay for faster scraping (be considerate)
python -m scraper.cli --days 1 --delay 0.5
```

## Output

One Markdown file per channel, named:

```
posts_<channel_name>_<start_date>_<end_date>.md
```

Example: `posts_habr_com_2026-04-22_2026-04-29.md`

Each file contains posts grouped by date, with timestamps and preserved hyperlinks:

```markdown
# Posts from @habr_com | 2026-04-22 – 2026-04-29

Source: https://t.me/s/habr_com

---

## 2026-04-22

**[Post 68439](https://t.me/habr_com/68439)** — 18:05

Post text with any inline links preserved.

**Links:**
- [Read the article](https://habr.com/ru/articles/12345/)
```

## Running Tests

```bash
python -m pytest tests/ -v
```

The test suite has 56 tests covering all modules. Tests use a real captured fixture page (`tests/fixtures/sample_page.html`) and mocked HTTP for network-dependent tests.

## Notes

- Only **public** Telegram channels (accessible via `t.me/s/<name>`) are supported.
- The scraper paginates backwards through a channel's history using Telegram's `?before=<id>` parameter, fetching up to 50 pages per channel as a safety cap.
- A 1-second delay between requests is applied by default. Reduce it carefully — aggressive scraping may trigger rate limits (HTTP 429).
- If a channel fails (network error, 404, etc.), the scraper skips it, logs a warning, and continues with remaining channels. Exit code is `1` if any channel failed.
- All output files are UTF-8 encoded.
