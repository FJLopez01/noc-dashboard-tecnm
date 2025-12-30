import json
from pathlib import Path

SEGMENTS_FILE = Path("data/segments.json")

def load_segments():
    if not SEGMENTS_FILE.exists():
        return []

    with open(SEGMENTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("segments", [])


def save_segments(segments):
    with open(SEGMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump({"segments": segments}, f, indent=4)