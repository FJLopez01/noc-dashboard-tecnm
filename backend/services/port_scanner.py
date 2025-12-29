import socket

DEFAULT_PORTS = [22, 80, 443, 3306, 53]

def scan_ports(ip, ports=DEFAULT_PORTS, timeout=0.5):
    results = []

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            status = "CLOSED"
            try:
                if sock.connect_ex((ip, port)) == 0:
                    status = "OPEN"
            except Exception:
                status = "CLOSED"

            results.append(f"{port}:{status}")

    return "|".join(results)