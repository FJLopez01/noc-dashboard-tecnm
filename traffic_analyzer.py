# traffic_analyzer.py
from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict
import threading
import time

# Estructura de datos global para guardar estadísticas
traffic_data = {
    "top_ips": defaultdict(int),
    "top_ports": defaultdict(int),
    "total_bytes": 0
}

# Mapeo de puertos comunes a nombres (para que se vea bonito)
PORT_MAP = {
    80: "HTTP", 443: "HTTPS", 53: "DNS", 22: "SSH",
    3306: "MySQL", 5432: "Postgres", 5000: "Flask API",
    445: "SMB", 3389: "RDP"
}

def process_packet(packet):
    global traffic_data
    
    # Solo nos interesa IP (IPv4)
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        length = len(packet)

        # Sumar bytes totales
        traffic_data["total_bytes"] += length

        # Contar tráfico por IP (Origen y Destino cuentan)
        traffic_data["top_ips"][src_ip] += length
        traffic_data["top_ips"][dst_ip] += length

        # Identificar Protocolos/Puertos
        if TCP in packet:
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            # Usar el nombre si existe, si no "PORT-XXX"
            s_name = PORT_MAP.get(sport, f"TCP/{sport}")
            d_name = PORT_MAP.get(dport, f"TCP/{dport}")
            traffic_data["top_ports"][s_name] += length
            traffic_data["top_ports"][d_name] += length
            
        elif UDP in packet:
            sport = packet[UDP].sport
            dport = packet[UDP].dport
            s_name = PORT_MAP.get(sport, f"UDP/{sport}")
            d_name = PORT_MAP.get(dport, f"UDP/{dport}")
            traffic_data["top_ports"][s_name] += length
            traffic_data["top_ports"][d_name] += length

def start_sniffer_thread():
    """Inicia la captura en segundo plano"""
    t = threading.Thread(target=lambda: sniff(prn=process_packet, store=False))
    t.daemon = True # Se muere cuando cierras la app principal
    t.start()

def get_traffic_stats():
    """Devuelve los datos formateados para el frontend"""
    # Ordenamos para mandar solo el Top 5
    sorted_ips = sorted(traffic_data["top_ips"].items(), key=lambda x: x[1], reverse=True)[:5]
    sorted_ports = sorted(traffic_data["top_ports"].items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "total_mb": round(traffic_data["total_bytes"] / (1024 * 1024), 2),
        "ips": [{"ip": k, "bytes": v} for k, v in sorted_ips],
        "protocols": [{"name": k, "bytes": v} for k, v in sorted_ports]
    }