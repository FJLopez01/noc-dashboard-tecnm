# backend/services/inventory_loader.py

# Obtiene los segmentos de red guardados (ej. 192.168.1.0/24)
from backend.services.segment_loader import load_segments

# Escanea esos segmentos y detecta hosts activos
from backend.services.network_discovery import discover_hosts

def load_hosts():
    """
    Carga el inventario de hosts a partir de los segmentos configurados.
    Si no existen segmentos definidos, retorna una lista vacía.
    """

    # Obtener segmentos de red definidos por el usuario
    segments = load_segments()

    # Si no hay segmentos, no hay hosts que descubrir
    if not segments:
        return []

    # Ejecutar descubrimiento automático en los segmentos
    discovered_hosts = discover_hosts(segments)

    # Retornar lista de hosts descubiertos
    return discovered_hosts
