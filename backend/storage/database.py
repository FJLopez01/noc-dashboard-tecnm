import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/history.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS latency_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                latency_ms INTEGER,
                timestamp TEXT NOT NULL
            )
        """)
        
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
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO latency_history (ip, latency_ms, timestamp)
            VALUES (?, ?, ?)
        """, (ip, latency_ms, datetime.utcnow().isoformat()))
        conn.commit()
        
        
def insert_uptime(ip, is_online):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO uptime_history (ip, is_online, timestamp)
            VALUES (?, ?, ?)
        """, (ip, int(is_online), datetime.utcnow().isoformat()))
        conn.commit()


def get_last_latencies(ip, limit=20):
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

    # Se invierte para orden cronológico (frontend)
    return [
        {"timestamp": ts, "latency_ms": lat}
        for ts, lat in reversed(rows)
    ]