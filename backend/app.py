from flask import Flask, render_template

# Blueprints API
from backend.api.status import bp as status_bp
from backend.api.history import bp as history_bp
from backend.api.export import export_bp
from backend.api.segments import bp as segments_bp
from backend.api.traffic import bp as traffic_bp

# Inicialización de base de datos
from backend.storage.database import init_db


def create_app():
    """
    Application Factory.
    Crea y configura la aplicación Flask del NOC Dashboard.
    """
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # ---------- FRONTEND ----------
    @app.route("/")
    def index():
        """
        Ruta principal que renderiza el dashboard.
        """
        return render_template("index.html")

    # ---------- API ----------
    app.register_blueprint(status_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(segments_bp)
    app.register_blueprint(traffic_bp)

    # ---------- BASE DE DATOS ----------
    # Crea las tablas necesarias si no existen
    init_db()

    return app