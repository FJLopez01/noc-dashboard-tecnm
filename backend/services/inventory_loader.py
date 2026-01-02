# backend/services/inventory_loader.py

from backend.services.segment_loader import load_segments
from backend.services.network_discovery import discover_hosts

def load_hosts():
    segments = load_segments()
    if not segments:
        return []

    discovered_hosts = discover_hosts(segments)

    return discovered_hosts
