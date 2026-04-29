import os
from datetime import datetime


def build_filename(channel_name: str, start: datetime, end: datetime) -> str:
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    return f"posts_{channel_name}_{start_str}_{end_str}.md"


def write_markdown(content: str, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
