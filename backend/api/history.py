from flask import Blueprint, jsonify
from backend.storage.database import get_last_latencies

bp = Blueprint("history", __name__, url_prefix="/api")

@bp.route("/history/<ip>", methods=["GET"])
def history(ip):
    data = get_last_latencies(ip)
    return jsonify(data)