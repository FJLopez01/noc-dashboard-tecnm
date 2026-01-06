# backend/api/export.py

# Importa el módulo csv para generar archivos CSV
import csv

# StringIO permite manejar texto en memoria como si fuera un archivo
from io import StringIO

# Blueprint: modulariza rutas en Flask
# Response: permite devolver respuestas HTTP personalizadas
from flask import Blueprint, Response

# Se obtiene el estado actual de los hosts desde memoria (no BD)
from backend.storage.memory_store import get_all_hosts


# Se define un Blueprint para el módulo de exportación
# url_prefix="/api" hace que la ruta final sea /api/export
export_bp = Blueprint("export", __name__, url_prefix="/api")


# Ruta GET para exportar la información del dashboard a CSV
@export_bp.route("/export", methods=["GET"])
def export_csv():
    # Obtiene todos los hosts monitoreados desde el memory_store
    hosts = get_all_hosts()

    # Se crea un buffer de texto en memoria
    output = StringIO()

    # Se inicializa el escritor CSV usando el buffer
    writer = csv.writer(output)

    # Se escribe el encabezado del CSV (columnas)
    # Este formato es profesional y fácil de abrir en Excel
    writer.writerow([
        "IP Address",
        "Hostname",
        "Status",
        "Latency (ms)",
        "Uptime (%)",
        "Critical",
        "Last Check"
    ])

    # Se recorren todos los hosts para escribir una fila por cada uno
    for h in hosts:
        writer.writerow([
            h.get("ip_address"),          # Dirección IP del host
            h.get("host_name"),           # Nombre o alias del host
            h.get("status"),              # Estado: online / offline
            h.get("latency_ms"),           # Latencia en milisegundos
            h.get("uptime_percent"),       # Porcentaje de uptime
            "YES" if h.get("critical") else "NO",  # Indicador crítico
            h.get("last_check") or h.get("timestamp")  # Última verificación
        ])

    # Se construye la respuesta HTTP con el contenido CSV
    response = Response(
        output.getvalue(),   # Contenido completo del CSV
        mimetype="text/csv"  # Tipo de archivo
    )

    # Header que fuerza la descarga del archivo en el navegador
    response.headers["Content-Disposition"] = (
        "attachment; filename=noc_dashboard_export.csv"
    )

    # Se devuelve el archivo CSV al cliente
    return response