# backend/api/auth.py

import os
from functools import wraps
from flask import request, jsonify


def require_api_key(f):
    """
    Decorador que protege un endpoint exigiendo
    un API Key válido en el header X-API-Key.

    Uso:
        @bp.get("/status")
        @require_api_key
        def status():
            ...

    Configuración:
        Variable de entorno NOC_API_KEY debe estar
        definida antes de iniciar la aplicación.
        Si no está definida, el arranque falla con
        un error explícito (ver create_app).
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-API-Key", "").strip()
        expected = os.environ.get("NOC_API_KEY", "")

        if not token or token != expected:
            return jsonify({"error": "Unauthorized"}), 401

        return f(*args, **kwargs)

    return decorated
