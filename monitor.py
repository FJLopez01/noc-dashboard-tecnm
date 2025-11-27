import ping3
import time
import os
from database import save_ping_result, init_db
from net_tools import scan_services  # <--- MODULARIDAD

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

def get_targets():
    targets = []
    if not os.path.exists("ips.txt"): return []

    with open("ips.txt", 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.strip().split(',')
                ip = parts[0].strip()
                name = parts[1].strip() if len(parts) > 1 else ip
                
                # Obtener puertos si existen (tercera columna)
                ports = []
                if len(parts) > 2:
                    # Separamos por espacio "80 443" -> [80, 443]
                    raw_ports = parts[2].strip().split()
                    ports = [p for p in raw_ports if p.isdigit()]

                targets.append({'ip': ip, 'name': name, 'ports': ports})
    return targets

if __name__ == "__main__":
    print("--- MONITOR DE SERVICIOS INICIADO ---")
    while True:
        target_list = get_targets()
        
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