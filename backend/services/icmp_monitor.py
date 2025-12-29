import ping3

ping3.EXCEPTIONS = True

def ping_host(ip, timeout=1):
    try:
        latency = ping3.ping(ip, timeout=timeout)
        if latency is None:
            return False, None
        return True, int(latency * 1000)
    except Exception:
        return False, None
