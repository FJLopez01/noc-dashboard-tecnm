# backend/api/segments.py

# Blueprint permite agrupar rutas relacionadas (segmentos de red)
# request se usa para leer datos enviados por el frontend
# jsonify convierte respuestas Python a JSON
from flask import Blueprint, request, jsonify

# Librería estándar para validar y trabajar con redes IP (CIDR)
import ipaddress


# Importa funciones de negocio para manejar segmentos
# Estas funciones encapsulan la lógica (archivo, BD, etc.)
from backend.services.segment_loader import (
    load_segments,
    save_segments,
    delete_segment
)


# Blueprint del módulo de segmentos
# Todas las rutas quedan bajo /api
bp = Blueprint("segments", __name__, url_prefix="/api")


@bp.route("/segments", methods=["GET"])
def get_segments():
    # Carga los segmentos desde el servicio
    # (pueden venir de archivo o base de datos)
    return jsonify(load_segments())



@bp.route("/segments", methods=["POST"])
def add_segment():
    # Datos enviados en formato JSON
    data = request.json

    # Segmento esperado, ejemplo: "192.168.1.0/24"
    segment = data.get("segment")

    try:
        # Verifica que sea una red IP válida (CIDR)
        ipaddress.ip_network(segment)
    except Exception:
        # Si no es válida, responde con error HTTP 400
        return jsonify({"error": "Segmento inválido"}), 400

    segments = load_segments()

    if segment not in segments:
        segments.append(segment)
        save_segments(segments)

    return jsonify({"ok": True, "segments": segments})


@bp.route("/segments/<path:segment>", methods=["DELETE"])
def remove_segment(segment):
    if delete_segment(segment):
        return jsonify({"ok": True})
    return jsonify({"error": "Segmento no encontrado"}), 404
