# backend/api/status.py

from flask import Blueprint, jsonify

from backend.storage.memory_store import get_all_hosts
from backend.services.uptime_calculator import calculate_uptime_batch
from backend.api.auth import require_api_key

bp = Blueprint("status", __name__, url_prefix="/api")


@bp.get("/status")
@require_api_key
def status():
    """
    Devuelve el estado actual de todos los hosts
    enriquecido con el uptime calculado en batch.

    ANTES: N queries SQLite (una por host)
    AHORA: 1 query SQLite para todos los hosts
    """
    hosts = get_all_hosts()

    if not hosts:
        return jsonify([])

    # ── Batch: una sola query para todos los hosts ─────────────
    ips            = [h["ip_address"] for h in hosts]
    uptime_by_ip   = calculate_uptime_batch(ips)

    # ── Enriquecer cada host con su uptime ─────────────────────
    for host in hosts:
        host["uptime_percent"] = uptime_by_ip.get(host["ip_address"], 100.0)

    return jsonify(hosts)
