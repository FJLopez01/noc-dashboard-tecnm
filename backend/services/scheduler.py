import threading
import time
from datetime import datetime

from backend.services.icmp_monitor import ping_host
from backend.storage.database import get_connection
from backend.config import HOSTS, PING_INTERVAL


def monitor_loop():
    """
    Loop principal de monitoreo.
    Ejecuta ping periódico a todos los hosts configurados.
    """
    print("[SCHEDULER] Monitor de red iniciado")

    while True:
        for host in HOSTS:
            ip = host["ip"]
            name = host.get("name", ip)

            try:
                latency = ping_host(ip)
                timestamp = datetime.utcnow().isoformat()

                with get_connection() as conn:
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO latency_history (ip, latency_ms, timestamp)
                        VALUES (?, ?, ?)
                    """, (ip, latency, timestamp))

                    conn.commit()

                status = "ONLINE" if latency is not None else "OFFLINE"
                print(f"[{timestamp}] {name} ({ip}) → {status} {latency}ms")

            except Exception as e:
                print(f"[SCHEDULER] Error monitoreando {name} ({ip}): {e}")

        time.sleep(PING_INTERVAL)