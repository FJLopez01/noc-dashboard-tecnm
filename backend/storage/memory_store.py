from collections import defaultdict
from datetime import datetime

# Estado actual de cada host
HOST_STATUS = {}

# Historial básico para uptime
UPTIME_DATA = defaultdict(lambda: {
    "total_checks": 0,
    "online_checks": 0
})

def update_uptime(ip, is_online):
    data = UPTIME_DATA[ip]
    data["total_checks"] += 1
    if is_online:
        data["online_checks"] += 1

def get_uptime_percent(ip):
    data = UPTIME_DATA[ip]
    if data["total_checks"] == 0:
        return 100.0
    return (data["online_checks"] / data["total_checks"]) * 100

def update_host_status(ip, payload):
    payload["timestamp"] = datetime.utcnow().isoformat()
    HOST_STATUS[ip] = payload

def get_all_hosts():
    return list(HOST_STATUS.values())
