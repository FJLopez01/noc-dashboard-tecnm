from backend.app import create_app
from backend.services.scheduler import monitor_loop
import threading

app = create_app()

# Lanzar scheduler en background
scheduler_thread = threading.Thread(target=monitor_loop, daemon=True)
scheduler_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
