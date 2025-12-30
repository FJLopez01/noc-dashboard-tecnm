````markdown
# 🖥️ NOC Dashboard – Network Monitoring System

Sistema de monitoreo de infraestructura de red (NOC) desarrollado en Python, diseñado para supervisar **disponibilidad, latencia, servicios y tráfico de red**, inspirado en herramientas empresariales como Zabbix, Nagios y NetFlow.

El proyecto implementa una **arquitectura modular**, separando claramente la recolección de métricas, la persistencia de datos, la API y la visualización.

---

## 🚀 Características Principales

### ✅ Monitoreo de Disponibilidad (ICMP)
- Verificación periódica de estado **Online / Offline**
- Medición de **latencia en milisegundos**
- Registro histórico en base de datos

### ✅ Inspección de Servicios (Capa 4)
- Escaneo TCP de puertos configurables por host
- Validación de servicios críticos (HTTP, HTTPS, SSH, DNS, SQL)

### ✅ Cálculo de SLA / Uptime
- Métrica de disponibilidad basada en **tiempo real**
- Cálculo histórico configurable (últimas 24h por defecto)
- Implementación basada en diferencias temporales (no contadores simples)

### ✅ Análisis de Red en Tiempo Real
- Estado actual almacenado en memoria (RAM)
- API rápida sin impacto en la red
- Arquitectura preparada para integración NetFlow (Scapy)

### ✅ Descubrimiento de Red
- Detección automática de hosts activos en la red
- Resolución de hostname
- Inventario persistente en JSON sin duplicados

### ✅ Reportes
- Exportación de métricas históricas a CSV
- Latencia promedio y SLA por host

---

## 🏗️ Arquitectura del Sistema

```text
Scheduler (Thread en background)
 ├─ ICMP Ping
 ├─ Port Scan
 ├─ Cálculo de métricas
 ├─ Persistencia (SQLite)
 └─ Estado actual (RAM)

Flask API
 ├─ /api/status      → Estado actual desde memoria
 ├─ /api/history/ip  → Históricos de latencia
 └─ /api/export      → Reportes CSV

Frontend
 └─ Dashboard web con KPIs y gráficas
````

### 📌 Principios de diseño

* El **API no ejecuta tareas de red**
* El **scheduler es la única fuente de monitoreo**
* La memoria se usa para **tiempo real**
* La base de datos se usa para **histórico y SLA**

---

## 📂 Estructura del Proyecto

```text
noc-dashboard/
│
├── backend/
│   ├── services/        # Lógica de negocio (ping, scan, scheduler)
│   ├── api/             # Endpoints REST
│   ├── storage/         # Persistencia (SQLite + RAM)
│   └── config.py
│
├── frontend/
│   ├── templates/       # HTML
│   └── static/          # JS, CSS
│
├── data/
│   ├── hosts.json       # Inventario
│   └── history.db      # Métricas históricas
│
├── docs/
│   ├── architecture.md
│   └── screenshots/
│
├── run.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Tecnologías Utilizadas

* **Python 3**
* **Flask**
* **SQLite**
* **ping3**
* **Sockets TCP**
* **Threading / ThreadPoolExecutor**
* **Scapy (NetFlow – en progreso)**
* **HTML / CSS / JavaScript**

---

## ▶️ Ejecución del Proyecto

### 1️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecutar el sistema

```bash
python run.py
```

### 3️⃣ Acceder al dashboard

```
http://localhost:5000
```

---

## 📈 Ejemplo de Métricas

* Latencia promedio por host
* Estado actual de servicios
* SLA porcentual (últimas 24h)
* Historial gráfico de latencia

---

## 🔒 Consideraciones de Seguridad

* El escaneo de red se ejecuta solo en entornos controlados
* El sistema no ejecuta acciones destructivas
* Diseñado para redes locales y laboratorios

---

## 🧠 Aprendizajes Clave

* Diseño de sistemas de monitoreo
* Separación correcta entre recolección y visualización
* Manejo de métricas históricas
* Arquitectura escalable basada en eventos
* Networking (ICMP, TCP, SLA, Discovery)

---

## 📌 Roadmap

* Integración completa de NetFlow con Scapy
* Alertas por umbral (email / webhook)
* Autenticación y roles
* Dashboard avanzado con filtros

---

## 👨‍💻 Autores

**Frank Joseph López Cruz**
Ingeniería en Datos e Inteligencia Organizacional

**Eduardo Mauricio Garrido Rodriguez**
Ingeniería en Datos e Inteligencia Organizacional

Este proyecto fue desarrollado como parte de un portafolio profesional enfocado en **infraestructura, monitoreo y análisis de datos**.

