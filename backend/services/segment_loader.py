# backend/services/segment_loader.py

import json
import os
from pathlib import Path
from backend.config import SEGMENTS_FILE

SEGMENTS_PATH = Path(SEGMENTS_FILE)

def load_segments():
    if not SEGMENTS_PATH.exists():
        return []

    with SEGMENTS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("segments", [])

def save_segments(segments):
    SEGMENTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with SEGMENTS_PATH.open("w", encoding="utf-8") as f:
        json.dump({"segments": segments}, f, indent=4)

def delete_segment(segment):
    segments = load_segments()

    if segment in segments:
        segments.remove(segment)
        save_segments(segments)
        return True

    return False

def segments_last_modified():
    if not os.path.exists(SEGMENTS_FILE):
        return 0
    return os.path.getmtime(SEGMENTS_FILE)