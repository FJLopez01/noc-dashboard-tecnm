import subprocess
import platform
import socket
import re
from concurrent.futures import ThreadPoolExecutor
import nmap # pip install python-nmap

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
        return {"ip": ip, "name": hostname, "ports": None}
    return None

def escanear_red():
    base_ip = "192.168.0."
    
    ips = [base_ip + str(i) for i in range(1, 256)]
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        resultados = list(executor.map(scan_device, ips))
    
    resultados = [x for x in resultados if x is not None]
    
    with open("ips.txt", "w") as archivo:
        for resultado in resultados:
            archivo.write(f"{resultado['ip'], resultado['name']}\n")

    return resultados
