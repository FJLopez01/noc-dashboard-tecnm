from flask import Blueprint, request, jsonify
import ipaddress

from backend.services.segment_loader import load_segments, save_segments

bp = Blueprint("segments", __name__, url_prefix="/api")


@bp.route("/segments", methods=["GET"])
def get_segments():
    return jsonify(load_segments())


@bp.route("/segments", methods=["POST"])
def add_segment():
    data = request.json
    segment = data.get("segment")

    try:
        ipaddress.ip_network(segment)
    except Exception:
        return jsonify({"error": "Segmento inválido"}), 400

    segments = load_segments()

    if segment not in segments:
        segments.append(segment)
        save_segments(segments)

    return jsonify({"ok": True, "segments": segments})