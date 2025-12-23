import ping3
import time
import os
from database import save_ping_result, init_db
from net_tools import scan_services  # <--- MODULARIDAD
from test_socket import escanear_red
import re

if not os.path.exists("network_monitor.db"):
    init_db()

def limpiar_pantalla():
    # 'nt' es para Windows, 'posix' para Linux y macOS
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def check_host(ip):
    try:
        delay = ping3.ping(ip, unit='ms')
        if delay is False or delay is None:
            return "offline", None
        else:
            return "online", round(delay, 2)
    except:
        return "error", None

def main():
    print("--- MONITOR DE SERVICIOS INICIADO ---")
    res = 'n'
    while True:
        while res.lower() == 'n':
            segmento = input("Introduzca el segmento de red a escanear (ejemplo: 192.168.0)\n")
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}$', segmento):
                print("Segmento de red inválido.")
            else:
                break

        target_list = escanear_red(segmento)
        
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

        res = input("¿Continuar escaneando el mismo segmento? Y/N\n")
        limpiar_pantalla()
        if res.lower() == 'y':
            print("Reiniciando escaneo del mismo segmento...")
            time.sleep(5)
        else:
            res = 'n'
            continue

if __name__ == "__main__":
    main()