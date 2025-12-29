from datetime import datetime, timedelta
from backend.storage.database import get_connection

def calculate_uptime(ip, hours=24):
    since = datetime.utcnow() - timedelta(hours=hours)

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

    if len(rows) < 2:
        return 100.0  # No suficiente data, asumimos OK

    online_time = 0
    total_time = 0

    for i in range(len(rows) - 1):
        state, t1 = rows[i]
        _, t2 = rows[i + 1]

        delta = (
            datetime.fromisoformat(t2) -
            datetime.fromisoformat(t1)
        ).total_seconds()

        total_time += delta
        if state == 1:
            online_time += delta

    if total_time == 0:
        return 100.0

    return round((online_time / total_time) * 100, 2)