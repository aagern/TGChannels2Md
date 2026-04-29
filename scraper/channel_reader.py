from typing import List
from urllib.parse import urlparse


def read_channels(filepath: str) -> List[str]:
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            result.append(stripped)
    return result


def extract_channel_name(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc != "t.me":
        raise ValueError(f"Not a t.me URL: {url}")
    path = parsed.path.rstrip("/")
    parts = path.split("/")
    if len(parts) < 3 or parts[1] != "s":
        raise ValueError(f"URL does not match t.me/s/<channel> pattern: {url}")
    return parts[2]
