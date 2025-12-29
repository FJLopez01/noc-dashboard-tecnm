import csv
import os
from datetime import datetime
from flask import Blueprint, send_file

from backend.services.uptime_calculator import calculate_uptime
from backend.storage.database import get_connection
from backend.config import HOSTS

export_bp = Blueprint("export", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXPORT_DIR = os.path.join(BASE_DIR, "data", "exports")

@export_bp.route("/api/export", methods=["GET"])
def export_csv():
    os.makedirs(EXPORT_DIR, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"noc_report_{timestamp}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "ip",
            "status",
            "avg_latency_ms",
            "sla_percent",
            "generated_at"
        ])

        for host in HOSTS:
            ip = host["ip"]
            sla = calculate_uptime(ip)

            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT AVG(latency_ms)
                    FROM latency_history
                    WHERE ip = ?
                """, (ip,))
                avg_latency = cursor.fetchone()[0]

            status = "Online" if avg_latency is not None else "Offline"

            writer.writerow([
                ip,
                status,
                round(avg_latency, 2) if avg_latency else "",
                sla,
                timestamp
            ])

    return send_file(filepath, as_attachment=True)