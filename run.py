from backend.app import create_app
from backend.services.scheduler import monitor_loop
from backend.services.traffic_analyzer import start_sniffer_thread
import threading

# Crear la aplicación Flask
app = create_app()

# ---------- SCHEDULER DE MONITOREO ----------
# Ejecuta el monitoreo de hosts (ICMP, latencia, puertos)
# en un hilo separado para no bloquear Flask
scheduler_thread = threading.Thread(
    target=monitor_loop,
    daemon=True
)
scheduler_thread.start()

# ---------- NETFLOW / CAPTURA DE TRÁFICO ----------
# Inicia el sniffer de paquetes (Scapy) en segundo plano
start_sniffer_thread()

# ---------- SERVIDOR WEB ----------
if __name__ == "__main__":
    # Iniciar servidor Flask
    app.run(debug=True)
