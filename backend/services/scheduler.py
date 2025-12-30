# backend/services/scheduler.py

import time
from datetime import datetime

from backend.services.icmp_monitor import ping_host
from backend.services.port_scanner import scan_ports
from backend.services.inventory_loader import load_hosts
from backend.storage.database import insert_latency, insert_uptime
from backend.storage.memory_store import update_host_status
from backend.config import PING_INTERVAL

DISCOVERY_INTERVAL = 300  # 5 minutos


def monitor_loop():
    print("[SCHEDULER] Monitor iniciado")

    last_inventory_reload = 0
    hosts = []

    while True:
        now = time.time()

        # 🔄 Reload inventario
        if now - last_inventory_reload > DISCOVERY_INTERVAL:
            hosts = load_hosts()
            last_inventory_reload = now
            print(f"[SCHEDULER] Hosts cargados: {len(hosts)}")

        for host in hosts:
            ip = host["ip"]
            name = host.get("name", ip)
            services_cfg = host.get("services", [])

            is_online, latency = ping_host(ip)
            timestamp = datetime.utcnow().isoformat()

            insert_uptime(ip, is_online)

            if is_online and latency is not None:
                insert_latency(ip, latency)

            services = (
                scan_ports(ip, services_cfg) if is_online else ""
            )

            update_host_status(ip, {
                "ip_address": ip,
                "host_name": name,
                "status": "online" if is_online else "offline",
                "latency_ms": latency or 0,
                "services": services,
                "timestamp": timestamp
            })

            print(f"[{timestamp}] {ip} → {'ONLINE' if is_online else 'OFFLINE'}")

        time.sleep(PING_INTERVAL)