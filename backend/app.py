from flask import Flask, render_template
from backend.api.status import bp as status_bp
from backend.api.history import bp as history_bp  
from backend.storage.database import init_db
from backend.api.export import export_bp
from backend.api.segments import bp as segments_bp
from backend.api.traffic import bp as traffic_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # ---------- FRONTEND ----------
    @app.route("/")
    def index():
        return render_template("index.html")

    # ---------- API ----------
    app.register_blueprint(status_bp)
    app.register_blueprint(history_bp) 
    app.register_blueprint(export_bp)
    app.register_blueprint(segments_bp)
    app.register_blueprint(traffic_bp)

    # ---------- INICIALIZAR DB ----------
    init_db()
    
    return app