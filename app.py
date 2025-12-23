import sqlite3
import csv
import io
import os
from flask import Flask, jsonify, render_template, Response
from monitor import main as monitor_main
import subprocess
# Importamos el módulo de tráfico (Asegúrate de tener traffic_analyzer.py creado)
from traffic_analyzer import start_sniffer_thread, get_traffic_stats

app = Flask(__name__)
DB_FILE = "network_monitor.db"
CONFIG_FILE = "ips.txt"

# --- INICIO DEL SNIFFER (Solo si no es reload) ---
if os.environ.get('WERKZEUG_RUN_MAIN') or not app.debug:
    try:
        start_sniffer_thread()
        print("--- SNIFFER DE RED (SCAPY) INICIADO ---")
    except Exception as e:
        print(f"Error iniciando sniffer (¿Eres admin?): {e}")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_active_ips():
    active_ips = []
    if not os.path.exists(CONFIG_FILE):
        return []
    try:
        with open(CONFIG_FILE, 'r') as f:
            for line in f:
                limpio = line.replace("(", "").replace(")", "").replace("'", "")
                ip = limpio.split(",")[0].strip()
                active_ips.append(ip)
    except Exception as e:
        print(f"Error config: {e}")
    return active_ips

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p1.ip_address, p1.host_name, p1.services, p1.status, p1.latency_ms, p1.timestamp,
            (SELECT COUNT(*) FROM ping_logs p2 WHERE p2.ip_address = p1.ip_address AND p2.status = 'online') * 100.0 / 
            (SELECT COUNT(*) FROM ping_logs p3 WHERE p3.ip_address = p1.ip_address) as uptime_percent
        FROM ping_logs p1
        WHERE p1.timestamp = (SELECT MAX(timestamp) FROM ping_logs p4 WHERE p4.ip_address = p1.ip_address)
        ORDER BY p1.ip_address
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    active_list = get_active_ips()
    all_data = [dict(row) for row in rows]
    filtered_data = [d for d in all_data if d['ip_address'] in active_list]
    
    return jsonify(filtered_data)

# --- NUEVA RUTA PARA NETFLOW (ESTA FALTABA) ---
@app.route('/api/traffic')
def api_traffic():
    # Obtiene los datos del hilo de Scapy
    return jsonify(get_traffic_stats())

@app.route('/api/history/<path:ip>')
def api_history(ip):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, latency_ms FROM ping_logs WHERE ip_address = ? ORDER BY timestamp DESC LIMIT 20', (ip,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows][::-1])

@app.route('/api/export')
def export_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ping_logs ORDER BY timestamp DESC LIMIT 1000')
    rows = cursor.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'IP', 'Nombre', 'Servicios', 'Fecha', 'Estado', 'Latencia'])
    for row in rows:
        writer.writerow([row['id'], row['ip_address'], row['host_name'], row['services'], row['timestamp'], row['status'], row['latency_ms']])
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=reporte_red_tecnm.csv"})

if __name__ == '__main__':
    #subprocess.Popen(['python', 'monitor.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    app.run(debug=True)