# Permite enviar paquetes ICMP directamente desde Python
import ping3

# Manejo de excepciones explícitas
ping3.EXCEPTIONS = True

def ping_host(ip, timeout=1):
    try:
        latency = ping3.ping(ip, timeout=timeout)
        
        # Host accesible
        if latency is None:
            return False, None
        return True, round(latency * 1000, 1)
    
    # Host inaccesible
    except ping3.errors.PingError:
        return False, None