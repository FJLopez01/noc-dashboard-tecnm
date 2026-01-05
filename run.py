from backend.app import create_app
from backend.services.scheduler import monitor_loop
from backend.services.traffic_analyzer import start_sniffer_thread
import threading

app = create_app()

# Scheduler uptime / servicios
scheduler_thread = threading.Thread(
    target=monitor_loop,
    daemon=True
)
scheduler_thread.start()

# NetFlow simulado
start_sniffer_thread()

if __name__ == "__main__":
    app.run(debug=True)
