import socket

# Puertos comunes a monitorear por defecto
DEFAULT_PORTS = [22, 80, 443, 3306, 53]

def scan_ports(ip, ports=DEFAULT_PORTS, timeout=0.5):
    """
    Escanea puertos TCP específicos en una IP.
    Retorna un string con el estado de cada puerto.
    Ejemplo: "22:OPEN|80:CLOSED"
    """
    results = []

    for port in ports:
        # Crear socket TCP IPv4
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Evitar bloqueos largos
            sock.settimeout(timeout)
            status = "CLOSED"

            try:
                # connect_ex retorna 0 si el puerto está abierto
                if sock.connect_ex((ip, port)) == 0:
                    status = "OPEN"
            except Exception:
                # Cualquier error se considera puerto cerrado
                status = "CLOSED"

            # Guardar resultado del puerto
            results.append(f"{port}:{status}")

    # Retornar resultados en formato compacto
    return "|".join(results)
