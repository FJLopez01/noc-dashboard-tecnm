import subprocess
import platform
import socket
from concurrent.futures import ThreadPoolExecutor
import json
import os

from backend.services.port_scanner import scan_ports

def get_hostname(ip):
    try:
        # Intenta obtener el nombre del dispositivo
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Desconocido"

def scan_device(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '500', ip]
    
    if subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        hostname = get_hostname(ip)
        services = scan_ports(ip)
        ports = []
        
        for service in services.split("|"):
            port, status = service.split(":")
            if status == "OPEN":
                ports.append(int(port))
            
            if port == "53":
                return {"ip": ip, "name": hostname, "type": "unknown", "critical": False, "services": ports}
                    
    return None


def save_scan(results):
    if os.path.exists('data/hosts.json') and os.path.getsize('data/hosts.json') > 0:
        with open('data/hosts.json', 'r') as hosts:
            data = json.load(hosts)
    else:
        data = []

    if isinstance(results, list):
        data.extend(results)
    else:
        data.append(results)

    with open('data/hosts.json', 'w') as hosts:
        json.dump(data, hosts, indent=4)
    return
    

def scan_network(segment):
    base_ip = segment + "."
    ips = [base_ip + str(i) for i in range(1, 256)]
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(scan_device, ips))
    
    results = [x for x in results if x is not None]
    
    return results 
