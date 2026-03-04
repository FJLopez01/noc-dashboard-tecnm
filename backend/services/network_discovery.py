# backend/services/network_discovery.py

import ipaddress
from concurrent.futures import ThreadPoolExecutor
from backend.services.icmp_monitor import ping_host


def discover_hosts(segments):
    """
    Descubre hosts activos en segmentos de red usando ICMP (ping).
    Retorna una lista de hosts vivos.
    """
    discovered = []

    # Función de prueba ICMP por IP
    def probe(ip):
        is_online, _ = ping_host(ip, timeout=0.3)
        return ip if is_online else None

    # Construir lista de IPs desde segmentos CIDR
    ips = []
    for segment in segments:
        network = ipaddress.ip_network(segment, strict=False)
        ips.extend(str(ip) for ip in network.hosts())

    # Escaneo concurrente para mejorar rendimiento
    with ThreadPoolExecutor(max_workers=50) as pool:
        results = pool.map(probe, ips)

    # Construir inventario base de hosts activos
    for ip in results:
        if ip:
            discovered.append({
                "ip": ip,
                "name": ip,
                "services": [],
                "critical": False,
                "type": "discovered"
            })

    return discovered
