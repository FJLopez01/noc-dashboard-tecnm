# backend/api/traffic.py

from flask import Blueprint, jsonify

from backend.services.traffic_analyzer import get_traffic_stats
from backend.api.auth import require_api_key

bp = Blueprint("traffic", __name__, url_prefix="/api")


@bp.route("/traffic", methods=["GET"])
@require_api_key
def traffic():
    return jsonify(get_traffic_stats())
