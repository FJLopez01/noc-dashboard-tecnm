## Descripción del Proyecto

Este sistema es una solución integral de monitoreo de infraestructura de red (NOC) diseñada para supervisar la disponibilidad, latencia y tráfico de servidores críticos.

A diferencia de un monitor ICMP tradicional, esta herramienta implementa un analizador de tráfico (Sniffer) basado en Scapy que opera a nivel de capa de red, permitiendo visualizar el consumo de ancho de banda y protocolos en tiempo real, similar a herramientas empresariales como NetFlow.

# Características Principales

* **Monitoreo de Disponibilidad (ICMP):** Verificación de estado *Online/Offline* y medición de latencia en ms.
* **Inspección de Servicios (Capa 4/7):** Escaneo de puertos TCP específicos (HTTP, SQL, SSH, DNS) para asegurar que los servicios estén operativos.
* **Análisis de Tráfico en Vivo (NetFlow):** Captura de paquetes en tiempo real para visualizar:
    * Top Consumidores (IPs).
    * Distribución de Protocolos (Gráficas de Dona).
    * Volumen total de datos transferidos.
* **Cálculo de SLA/Uptime:** Métrica de disponibilidad porcentual histórica por nodo.
* **Consola de Tráfico en Vivo:** Log de eventos estilo *Wireshark* directamente en el navegador.
* **Arquitectura Modular:** Separación estricta entre recolección de datos (Backend), API (Flask) y Visualización (Frontend).
* **Reportes:** Exportación de datos históricos a formato CSV.