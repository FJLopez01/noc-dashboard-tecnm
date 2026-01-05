# 🖥️ NOC Dashboard – Network Monitoring Platform

**NOC Dashboard** es una plataforma web de **monitoreo de red en tiempo real**, desarrollada para supervisar disponibilidad, servicios y tráfico de infraestructura IP.  
El sistema replica funcionalidades clave de un **Network Operations Center (NOC)** mediante una arquitectura modular y escalable.

📍 **Caso de uso:** Infraestructura del TecNM Cancún  
🎯 **Objetivo:** Visibilidad operacional, análisis de disponibilidad y tráfico, y generación de reportes.

---

## 🚀 Principales Capacidades

### 🔌 Network Availability Monitoring (ICMP)
- Detección de estado **Online / Offline**
- Medición de **latencia (ms)**
- Monitoreo continuo con actualización automática
- Persistencia de datos históricos

---

### 🧩 Service Monitoring (Layer 4 / 7)
- Escaneo de servicios TCP críticos:
  - HTTP / HTTPS
  - SSH
  - DNS
  - SQL (MySQL / PostgreSQL)
- Verificación de puertos **OPEN / CLOSED**
- Visualización directa por host

---

### 📡 Live Traffic Analysis (NetFlow Simulation)
- Captura de paquetes en tiempo real con **Scapy**
- Métricas generadas:
  - 🔝 Top 5 IPs consumidoras de tráfico
  - 📊 Distribución de protocolos (Donut Charts)
  - 💾 Volumen total de datos transferidos
- Renderizado dinámico sin recarga de página

> ⚠️ Requiere ejecución con privilegios de administrador para captura de tráfico.

---

### 📈 SLA & Uptime Calculation
- Cálculo histórico de disponibilidad por nodo
- Métrica porcentual de uptime
- Apoyo para análisis de cumplimiento de SLA

---

### 🖥 Live Traffic Console
- Consola en tiempo real estilo **Wireshark**
- Eventos ICMP y latencia
- Registro continuo de actividad
- Limpieza y control visual desde UI

---

### 📄 Reporting & Export
- Exportación de datos históricos en formato **CSV**
- Datos listos para:
  - Auditoría
  - Análisis externo
  - Reportes ejecutivos

---

## 🧱 System Architecture
noc-dashboard-tecnm/
│
├── backend/
│ ├── api/ # REST API endpoints
│ ├── services/ # ICMP, NetFlow, Scheduler
│ ├── storage/ # SQLite persistence
│ └── app.py # Flask app factory
│
├── frontend/
│ ├── templates/ # Jinja2 templates
│ └── static/
│ ├── css/
│ └── js/
│
├── run.py # Application entry point
├── requirements.txt
└── README.md

---

### Architectural Principles
- **Separation of Concerns**
- **Modular backend services**
- **Decoupled API & frontend**
- **Scalable design for production environments**

---

## 🛠️ Technology Stack

### Backend
- Python 3.11
- Flask
- Scapy
- Ping3
- APScheduler
- SQLite

### Frontend
- HTML5 / CSS3
- Bootstrap 5
- JavaScript (Fetch API)
- Chart.js
- Font Awesome

---

## ⚙️ Installation & Execution

### 1️⃣ Clone repository
```bash
git clone https://github.com/FJLopez01/noc-dashboard-tecnm.git
cd noc-dashboard-tecnm
```

### 2️⃣ Create virtual environment (Python 3.11)
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run application (Administrator privileges required)
```bash
python run.py
```

### Access via browser:
```bash
http://localhost:5000
```

## 🔐 Required Permissions

To enable Live Traffic Analysis (NetFlow):
- Run the application as Administrator
- Allow packet capture (Scapy)
- Without elevated privileges, traffic charts will not display data.

## 📌 Project Status

✔ Production-ready prototype
✔ Stable
✔ Academic & professional use
✔ Easily extensible (SNMP, alerts, auth, Docker)

## 👨‍💻 Authors

Frank Joseph López Cruz
Data Engineering & Organizational Intelligence
Universidad del Caribe
🔗 GitHub: https://github.com/FJLopez01

Eduardo Mauricio Garrido Rodríguez
Data Engineering & Organizational Intelligence
Universidad del Caribe

📄 License

Academic project for educational and demonstration purposes.
