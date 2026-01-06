# backend/api/status.py

# Blueprint permite agrupar rutas relacionadas
# jsonify transforma estructuras Python a JSON
from flask import Blueprint, jsonify

# Almacén en memoria donde se guarda el estado actual de los hosts
from backend.storage.memory_store import get_all_hosts

# Servicio encargado de calcular el uptime histórico de un host
from backend.services.uptime_calculator import calculate_uptime

# Esto registra el endpoint bajo /api/status
bp = Blueprint("status", __name__, url_prefix="/api")

# Devuelve el estado actual de todos los hosts enriquecido con uptime.
@bp.get("/status")
def status():
    # Obtener estado en tiempo real
    hosts = get_all_hosts()
    
    # Calcular uptime por host
    for h in hosts:
        h["uptime_percent"] = calculate_uptime(h["ip_address"])
    return jsonify(hosts)