# backend/services/inventory_loader.py

from backend.services.network_discovery import discover_hosts
from backend.config import NETWORK_SEGMENTS


def load_static_hosts():
    """
    Hosts definidos manualmente (infra crítica)
    """
    return [
        {
            "ip": "10.100.10.1",
            "name": "Gateway-10",
            "services": [22, 80],
            "critical": True,
            "type": "gateway"
        },
        {
            "ip": "10.100.11.1",
            "name": "Gateway-11",
            "services": [22, 80],
            "critical": True,
            "type": "gateway"
        }
    ]


def load_hosts():
    """
    Combina inventario estático + descubrimiento automático
    """
    static_hosts = load_static_hosts()
    discovered_hosts = discover_hosts(NETWORK_SEGMENTS)

    # Evitar duplicados por IP
    known_ips = {h["ip"] for h in static_hosts}

    merged = static_hosts.copy()
    for host in discovered_hosts:
        if host["ip"] not in known_ips:
            merged.append(host)

    return merged