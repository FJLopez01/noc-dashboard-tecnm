# backend/services/segment_loader.py

import json
import os
from pathlib import Path
from backend.config import SEGMENTS_FILE

# Ruta al archivo de segmentos configurados
SEGMENTS_PATH = Path(SEGMENTS_FILE)


def load_segments():
    """
    Carga los segmentos de red desde el archivo JSON.
    Retorna una lista de segmentos (CIDR).
    """
    # Si el archivo no existe, no hay segmentos configurados
    if not SEGMENTS_PATH.exists():
        return []

    # Leer y parsear el archivo JSON
    with SEGMENTS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Retornar solo la lista de segmentos
    return data.get("segments", [])


def save_segments(segments):
    """
    Guarda la lista de segmentos en el archivo JSON.
    Crea el directorio si no existe.
    """
    # Asegurar que el directorio exista
    SEGMENTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Guardar el archivo con formato legible
    with SEGMENTS_PATH.open("w", encoding="utf-8") as f:
        json.dump({"segments": segments}, f, indent=4)


def delete_segment(segment):
    """
    Elimina un segmento específico.
    Retorna True si fue eliminado, False si no existía.
    """
    segments = load_segments()

    if segment in segments:
        segments.remove(segment)
        save_segments(segments)
        return True

    return False


def segments_last_modified():
    """
    Retorna el timestamp de última modificación
    del archivo de segmentos.
    """
    if not os.path.exists(SEGMENTS_FILE):
        return 0

    return os.path.getmtime(SEGMENTS_FILE)