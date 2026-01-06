# backend\api\history.py

# Importa Blueprint para modularizar rutas Flask
# jsonify convierte estructuras Python (listas/dicts) a JSON HTTP
from flask import Blueprint, jsonify

# Importa la función que obtiene latencias históricas desde la BD
from backend.storage.database import get_last_latencies


# Se define el Blueprint del módulo de historial
# Todas las rutas quedarán bajo el prefijo /api
bp = Blueprint("history", __name__, url_prefix="/api")


# Endpoint que devuelve el historial de latencias de un host
# <ip> es un parámetro dinámico recibido desde la URL
@bp.route("/history/<ip>", methods=["GET"])
def history(ip):
    # Consulta en base de datos las últimas latencias del host
    data = get_last_latencies(ip)

    # Retorna la información en formato JSON
    # Este JSON es consumido directamente por el frontend (charts)
    return jsonify(data)