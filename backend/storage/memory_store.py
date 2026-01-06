from collections import defaultdict
from datetime import datetime

# Estado actual de cada host (cache en memoria)
# key   -> IP
# value -> último estado conocido del host
HOST_STATUS = {}

# Estructura ligera para cálculo básico de uptime en memoria
UPTIME_DATA = defaultdict(lambda: {
    "total_checks": 0,
    "online_checks": 0
})


def update_uptime(ip, is_online):
    """
    Actualiza los contadores de uptime para una IP.
    """
    data = UPTIME_DATA[ip]
    data["total_checks"] += 1

    if is_online:
        data["online_checks"] += 1


def get_uptime_percent(ip):
    """
    Retorna el porcentaje de uptime basado en los checks realizados.
    """
    data = UPTIME_DATA[ip]

    if data["total_checks"] == 0:
        return 100.0  # Sin datos aún, asumimos OK

    return (data["online_checks"] / data["total_checks"]) * 100


def update_host_status(ip, payload):
    """
    Actualiza el estado actual de un host en memoria.
    """
    payload["timestamp"] = datetime.utcnow().isoformat()
    HOST_STATUS[ip] = payload


def get_all_hosts():
    """
    Retorna el estado actual de todos los hosts.
    """
    return list(HOST_STATUS.values())