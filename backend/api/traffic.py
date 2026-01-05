from flask import Blueprint, jsonify
from backend.services.traffic_analyzer import get_traffic_stats

bp = Blueprint("traffic", __name__, url_prefix="/api")


@bp.route("/traffic", methods=["GET"])
def traffic():
    return jsonify(get_traffic_stats())
