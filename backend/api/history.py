# backend/api/history.py

from flask import Blueprint, jsonify

from backend.storage.database import get_last_latencies
from backend.api.auth import require_api_key

bp = Blueprint("history", __name__, url_prefix="/api")


@bp.route("/history/<ip>", methods=["GET"])
@require_api_key
def history(ip):
    data = get_last_latencies(ip)
    return jsonify(data)
