from flask import Blueprint, jsonify
from backend.services.icmp_monitor import ping_host
from backend.services.port_scanner import scan_ports
from backend.services.uptime_calculator import calculate_uptime
from backend.storage.memory_store import update_host_status, get_all_hosts
from backend.services.inventory_loader import load_hosts
from backend.storage.database import insert_latency, insert_uptime
from backend.services.uptime_calculator import calculate_uptime


bp = Blueprint("status", __name__, url_prefix="/api")

# Inventario inicial (después puede venir de JSON o DB)
HOSTS = load_hosts()

@bp.route("/status", methods=["GET"])
def get_status():
    for host in HOSTS:
        ip = host["ip"]
        name = host["name"]

        is_online, latency = ping_host(ip)
        services = scan_ports(ip, host["services"]) if is_online else ""

        insert_uptime(ip, is_online)

        if is_online and latency is not None:
            insert_latency(ip, latency)

        uptime = calculate_uptime(ip, is_online)

        payload = {
            "ip_address": ip,
            "host_name": name,
            "status": "online" if is_online else "offline",
            "latency_ms": latency,
            "uptime_percent": uptime,
            "services": services
        }

        update_host_status(ip, payload)

    return jsonify(get_all_hosts())
