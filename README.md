# NOC Dashboard - TecNM Cancún
### Sistema de Monitoreo de Red y Análisis de Tráfico en Tiempo Real

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Microframework-lightgrey)
![NetFlow](https://img.shields.io/badge/NetFlow-Scapy-orange)
![Status](https://img.shields.io/badge/Status-Stable-green)

---

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

---

# Arquitectura del Sistema

El proyecto sigue una arquitectura modular para facilitar el mantenimiento y la escalabilidad:

```text
dashboard-tecnm/
├── app.py                 # API Gateway & Servidor Web (Flask)
├── monitor.py             # Motor de Monitoreo Activo (Ping & Puertos)
├── traffic_analyzer.py    # Motor de Análisis Pasivo (Sniffer/Scapy)
├── net_tools.py           # Librería de utilidades de red (Sockets)
├── database.py            # Gestión de persistencia (SQLite)
├── requirements.txt       # Dependencias del proyecto
├── ips.txt                # Archivo de configuración de objetivos
├── static/
│   ├── css/               # Estilos Glassmorphism
│   └── js/                # Lógica Frontend Modular (netflow.js, dashboard.js)
└── templates/
    └── index.html         # Interfaz de Usuario

Requisitos Previos
Para ejecutar este sistema, se requiere:

Python 3.8+ instalado y agregado al PATH.

Npcap (Solo Windows): Necesario para que Scapy capture tráfico.

Importante: Instalar marcando la casilla "Install Npcap in WinPcap API-compatible Mode".

Descargar Npcap aquí.

Instalación
Clonar o descargar el repositorio:

Bash

git clone <url-del-repo>
cd dashboard-tecnm
Crear y activar el entorno virtual:

Bash

python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
Instalar dependencias:

Bash

pip install -r requirements.txt

---------

Ejecución del Sistema
El sistema consta de dos procesos que deben correr simultáneamente.


######################################################################
######################################################################

NOTA IMPORTANTE: Debido a que el módulo de NetFlow captura paquetes de la tarjeta de red, es necesario ejecutar la terminal o IDE como ADMINISTRADOR.

#######################################################################
#######################################################################

Paso 1: Configurar Hosts
Edite el archivo ips.txt para definir los objetivos: IP, NOMBRE, PUERTOS(opcional)

Plaintext

8.8.8.8, Google DNS, 53
192.168.1.254, Gateway Principal, 80 443
Paso 2: Iniciar el Monitor (Recolección de Datos)
Abra una terminal (Admin) y ejecute:

Bash

python monitor.py
Esto inicializará la base de datos y comenzará el escaneo activo.

Paso 3: Iniciar la Interfaz Web (API & NetFlow)
Abra otra terminal (Admin) y ejecute:

Bash

python app.py
Esto iniciará el servidor web y el hilo de captura de tráfico (Sniffer).

Paso 4: Acceder al Dashboard
Abra su navegador web y visite:

http://127.0.0.1:5000







