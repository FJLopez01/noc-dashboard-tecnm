# Blueprint permite organizar las rutas del backend
from flask import Blueprint, jsonify

# Servicio que analiza el tráfico de red capturado (NetFlow / ICMP / etc.)
from backend.services.traffic_analyzer import get_traffic_stats


bp = Blueprint("traffic", __name__, url_prefix="/api")

# Devuelve estadísticas de tráfico de red en tiempo real.
@bp.route("/traffic", methods=["GET"])
def traffic():
    # Obtención de estadísticas
    return jsonify(get_traffic_stats())
