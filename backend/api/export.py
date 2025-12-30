# backend/api/export.py

import csv
from io import StringIO
from flask import Blueprint, Response

from backend.storage.memory_store import get_all_hosts

export_bp = Blueprint("export", __name__, url_prefix="/api")


@export_bp.route("/export", methods=["GET"])
def export_csv():
    hosts = get_all_hosts()

    output = StringIO()
    writer = csv.writer(output)

    # Header profesional
    writer.writerow([
        "IP Address",
        "Hostname",
        "Status",
        "Latency (ms)",
        "Uptime (%)",
        "Critical",
        "Last Check"
    ])

    for h in hosts:
        writer.writerow([
            h.get("ip_address"),
            h.get("host_name"),
            h.get("status"),
            h.get("latency_ms"),
            h.get("uptime_percent"),
            "YES" if h.get("critical") else "NO",
            h.get("last_check") or h.get("timestamp")
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=noc_dashboard_export.csv"
    )

    return response
