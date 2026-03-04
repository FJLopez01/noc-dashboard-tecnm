# backend/api/segments.py

import ipaddress
from flask import Blueprint, request, jsonify

from backend.services.segment_loader import load_segments, save_segments, delete_segment
from backend.api.auth import require_api_key

bp = Blueprint("segments", __name__, url_prefix="/api")

MAX_SEGMENTS     = 20
MAX_NETWORK_SIZE = 1024  # máx ~4 subredes /24


@bp.route("/segments", methods=["GET"])
@require_api_key
def get_segments():
    return jsonify(load_segments())


@bp.route("/segments", methods=["POST"])
@require_api_key
def add_segment():
    data = request.json or {}
    segment = data.get("segment", "").strip()

    if not segment:
        return jsonify({"error": "Segmento requerido"}), 400

    try:
        network = ipaddress.ip_network(segment, strict=False)
    except ValueError:
        return jsonify({"error": "Segmento inválido"}), 400

    if network.num_addresses > MAX_NETWORK_SIZE:
        return jsonify({
            "error": f"Segmento demasiado grande (máx {MAX_NETWORK_SIZE} hosts)"
        }), 400

    segments = load_segments()

    if len(segments) >= MAX_SEGMENTS:
        return jsonify({
            "error": f"Límite de {MAX_SEGMENTS} segmentos alcanzado"
        }), 429

    if segment not in segments:
        segments.append(segment)
        save_segments(segments)

    return jsonify({"ok": True, "segments": segments})


@bp.route("/segments/<path:segment>", methods=["DELETE"])
@require_api_key
def remove_segment(segment):
    if delete_segment(segment):
        return jsonify({"ok": True})
    return jsonify({"error": "Segmento no encontrado"}), 404
