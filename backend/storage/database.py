import sqlite3
from pathlib import Path
from datetime import datetime

# Ruta del archivo de base de datos SQLite
DB_PATH = Path("data/history.db")


def get_connection():
    """
    Retorna una nueva conexión a la base de datos SQLite.
    """
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Inicializa las tablas necesarias para el sistema de monitoreo.
    Se ejecuta una sola vez al iniciar la aplicación.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # Historial de latencias por IP
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS latency_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                latency_ms INTEGER,
                timestamp TEXT NOT NULL
            )
        """)

        # Historial de estados (online/offline)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uptime_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                is_online INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        conn.commit()


def insert_latency(ip, latency_ms):
    """
    Inserta un registro de latencia para una IP específica.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO latency_history (ip, latency_ms, timestamp)
            VALUES (?, ?, ?)
        """, (ip, latency_ms, datetime.utcnow().isoformat()))
        conn.commit()


def insert_uptime(ip, is_online):
    """
    Inserta el estado online/offline de una IP.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO uptime_history (ip, is_online, timestamp)
            VALUES (?, ?, ?)
        """, (ip, int(is_online), datetime.utcnow().isoformat()))
        conn.commit()


def get_last_latencies(ip, limit=20):
    """
    Obtiene las últimas mediciones de latencia de una IP,
    ordenadas cronológicamente para el frontend.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, latency_ms
            FROM latency_history
            WHERE ip = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (ip, limit))
        rows = cursor.fetchall()

    # Se invierte el orden para graficar correctamente
    return [
        {"timestamp": ts, "latency_ms": lat}
        for ts, lat in reversed(rows)
    ]