import json
from pathlib import Path

HOSTS_FILE = Path("data/hosts.json")

def load_hosts():
    if not HOSTS_FILE.exists():
        raise FileNotFoundError("hosts.json no encontrado")

    with open(HOSTS_FILE, "r", encoding="utf-8") as f:
        hosts = json.load(f)

    validated = []
    for host in hosts:
        if "ip" not in host or "name" not in host:
            continue

        validated.append({
            "ip": host["ip"],
            "name": host["name"],
            "services": host.get("services", []),
            "critical": host.get("critical", False),
            "type": host.get("type", "unknown")
        })

    return validated