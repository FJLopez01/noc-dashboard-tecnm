import sqlite3

DB_FILE = "network_monitor.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ping_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            host_name TEXT,
            services TEXT,  -- NUEVA COLUMNA PARA SERVICIOS
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            latency_ms REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"BD Inicializada con soporte de Servicios.")

def save_ping_result(ip, name, services, status, latency):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ping_logs (ip_address, host_name, services, status, latency_ms) VALUES (?, ?, ?, ?, ?)",
        (ip, name, services, status, latency)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()