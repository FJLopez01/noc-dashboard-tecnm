# backend/api/status.py

from flask import Blueprint, jsonify
from backend.storage.memory_store import get_all_hosts
from backend.services.uptime_calculator import calculate_uptime

bp = Blueprint("status", __name__, url_prefix="/api")


@bp.get("/status")
def status():
    hosts = get_all_hosts()
    for h in hosts:
        h["uptime_percent"] = calculate_uptime(h["ip_address"])
    return jsonify(hosts)