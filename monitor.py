import ping3
import time
import os
from database import save_ping_result, init_db
from net_tools import scan_services  # <--- MODULARIDAD
from test_socket import escanear_red

if not os.path.exists("network_monitor.db"):
    init_db()

def check_host(ip):
    try:
        delay = ping3.ping(ip, unit='ms')
        if delay is False or delay is None:
            return "offline", None
        else:
            return "online", round(delay, 2)
    except:
        return "error", None

if __name__ == "__main__":
    print("--- MONITOR DE SERVICIOS INICIADO ---")
    while True:
        target_list = escanear_red()
        
        for target in target_list:
            ip = target['ip']
            name = target['name']
            ports = target['ports']
            
            # 1. Ping Básico
            status, latency = check_host(ip)
            
            # 2. Escaneo de Servicios (SOLO SI ESTÁ ONLINE)
            services_str = ""
            if status == 'online' and ports:
                print(f"Escaneando servicios para {name}...", end="")
                services_str = scan_services(ip, ports)
                print(" Hecho.")
            
            # 3. Guardar todo
            save_ping_result(ip, name, services_str, status, latency)
            
            print(f"{name} -> {status} | Servicios: {services_str}")

        print("Esperando 10 segundos...")
        time.sleep(10)