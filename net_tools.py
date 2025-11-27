# net_tools.py
import socket

def check_tcp_port(ip, port, timeout=1):
    """
    Intenta conectar a un puerto TCP específico.
    Retorna 'OPEN' si tiene éxito, 'CLOSED' si falla.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, int(port)))
        s.close()
        if result == 0:
            return "OPEN"
        else:
            return "CLOSED"
    except:
        return "ERROR"

def scan_services(ip, ports_list):
    """
    Recibe una IP y una lista de puertos (ej: [80, 443]).
    Retorna un string formateado: "80:OPEN|443:CLOSED"
    """
    if not ports_list:
        return ""
    
    results = []
    for port in ports_list:
        status = check_tcp_port(ip, port)
        # Guardamos formato "PUERTO:ESTADO"
        results.append(f"{port}:{status}")
    
    # Unimos todo con pipes para guardarlo fácil en la BD
    return "|".join(results)