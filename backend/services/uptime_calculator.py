from datetime import datetime, timedelta
from backend.storage.database import get_connection


def calculate_uptime(ip, hours=24):
    """
    Calcula el porcentaje de uptime de una IP
    basado en registros históricos de estado.
    
    :param ip: Dirección IP del host
    :param hours: Ventana de tiempo en horas (default 24)
    :return: Uptime en porcentaje
    """
    # Definir inicio del periodo de cálculo
    since = datetime.utcnow() - timedelta(hours=hours)

    # Obtener histórico de estados desde la base de datos
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT is_online, timestamp
            FROM uptime_history
            WHERE ip = ?
            AND timestamp >= ?
            ORDER BY timestamp ASC
        """, (ip, since.isoformat()))

        rows = cursor.fetchall()

    # Si no hay suficientes datos, se asume uptime completo
    if len(rows) < 2:
        return 100.0

    online_time = 0   # Segundos en estado online
    total_time = 0    # Segundos totales analizados

    # Recorrer los eventos consecutivos
    for i in range(len(rows) - 1):
        state, t1 = rows[i]
        _, t2 = rows[i + 1]

        # Diferencia de tiempo entre eventos
        delta = (
            datetime.fromisoformat(t2) -
            datetime.fromisoformat(t1)
        ).total_seconds()

        total_time += delta

        # Sumar solo si el host estaba online
        if state == 1:
            online_time += delta

    # Protección contra división entre cero
    if total_time == 0:
        return 100.0

    # Retornar uptime como porcentaje
    return round((online_time / total_time) * 100, 2)