# backend/services/traffic_analyzer.py

from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict
import threading

traffic_data = {
    "top_ips": defaultdict(int),
    "top_ports": defaultdict(int),
    "total_bytes": 0
}

PORT_MAP = {
    80: "HTTP",
    443: "HTTPS",
    53: "DNS",
    22: "SSH",
    3306: "MySQL",
    5432: "Postgres",
    5000: "Flask API",
    445: "SMB",
    3389: "RDP"
}


def process_packet(packet):
    if IP not in packet:
        return

    length = len(packet)
    traffic_data["total_bytes"] += length

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst

    traffic_data["top_ips"][src_ip] += length
    traffic_data["top_ips"][dst_ip] += length

    if TCP in packet:
        for port in (packet[TCP].sport, packet[TCP].dport):
            name = PORT_MAP.get(port, f"TCP/{port}")
            traffic_data["top_ports"][name] += length

    elif UDP in packet:
        for port in (packet[UDP].sport, packet[UDP].dport):
            name = PORT_MAP.get(port, f"UDP/{port}")
            traffic_data["top_ports"][name] += length


def start_sniffer_thread():
    t = threading.Thread(
        target=lambda: sniff(prn=process_packet, store=False),
        daemon=True
    )
    t.start()


def get_traffic_stats():
    top_ips = sorted(
        traffic_data["top_ips"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    top_ports = sorted(
        traffic_data["top_ports"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    return {
        "total_mb": round(traffic_data["total_bytes"] / (1024 * 1024), 2),
        "ips": [{"ip": ip, "bytes": b} for ip, b in top_ips],
        "protocols": [{"name": p, "bytes": b} for p, b in top_ports],
    }
