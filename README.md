```md
# 🖥️ NOC Dashboard – TecNM Cancún

Sistema de Monitoreo de Red (NOC – Network Operations Center) desarrollado para visualizar en tiempo real el estado, disponibilidad y tráfico de la infraestructura de red del **TecNM Cancún**.

El proyecto integra monitoreo ICMP, escaneo de servicios, análisis de tráfico tipo NetFlow y visualización web en tiempo real mediante una arquitectura modular Backend + API + Frontend.

---

## 🚀 Funcionalidades Principales

### 🔌 Monitoreo de Disponibilidad (ICMP)
- Verificación de estado **Online / Offline**
- Medición de **latencia en milisegundos**
- Actualización periódica automática
- Registro histórico de latencia

---

### 🧩 Inspección de Servicios (Capa 4 / 7)
- Escaneo de puertos TCP específicos:
  - HTTP (80)
  - HTTPS (443)
  - SSH (22)
  - DNS (53)
  - SQL (MySQL / PostgreSQL)
- Estado **OPEN / CLOSED**
- Visualización directa en el dashboard

---

### 📡 Análisis de Tráfico en Vivo (NetFlow Simulado)
- Captura de paquetes en tiempo real con **Scapy**
- Métricas mostradas:
  - 🔝 Top 5 IPs consumidoras de tráfico
  - 📊 Distribución de protocolos (gráficas de dona)
  - 💾 Volumen total de datos transferidos
- Actualización continua sin recargar la página

> ⚠️ Requiere permisos de administrador para captura de tráfico.

---

### 📈 Cálculo de SLA / Uptime
- Cálculo histórico de disponibilidad por nodo
- Métrica porcentual de uptime
- Visualización clara por host

---

### 🖥 Consola de Tráfico en Vivo
- Log estilo **Wireshark**
- Eventos ICMP en tiempo real
- Visualización clara de latencia y errores
- Control de limpieza de consola

---

### 📄 Reportes
- Exportación de datos históricos en formato **CSV**
- Información lista para auditoría o análisis externo

---

## 🧱 Arquitectura del Sistema

```

noc-dashboard-tecnm/
│
├── backend/
│   ├── api/                # Endpoints REST
│   ├── services/           # ICMP, NetFlow, Scheduler
│   ├── storage/            # Base de datos SQLite
│   └── app.py              # Inicialización Flask
│
├── frontend/
│   ├── templates/          # HTML (Jinja2)
│   └── static/
│       ├── css/
│       └── js/
│
├── run.py                  # Punto de entrada
├── requirements.txt
└── README.md

````

**Separación estricta de responsabilidades:**
- Backend → Recolección y procesamiento de datos
- API → Exposición de información
- Frontend → Visualización y experiencia de usuario

---

## 🛠️ Tecnologías Utilizadas

### Backend
- Python 3.11
- Flask
- Scapy
- Ping3
- APScheduler
- SQLite

### Frontend
- HTML5 + CSS3
- Bootstrap 5
- JavaScript (Fetch API)
- Chart.js
- Font Awesome

---

## ⚙️ Instalación y Ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/FJLopez01/noc-dashboard-tecnm.git
cd noc-dashboard-tecnm
````

### 2️⃣ Crear entorno virtual (Python 3.11)

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la aplicación (como Administrador)

```bash
python run.py
```

Acceder desde el navegador:

```
http://localhost:5000
```

---

## 🔐 Permisos Importantes

Para que el **análisis de tráfico (NetFlow)** funcione correctamente:

* Ejecutar la aplicación como **Administrador**
* Permitir captura de paquetes (Scapy)

En caso contrario, las gráficas de tráfico no mostrarán datos.

---

## 📌 Estado del Proyecto

✔ Funcional
✔ Estable
✔ Listo para entrega académica
✔ Escalable para producción

---

## 👨‍💻 Autores

**Frank Joseph López Cruz**
Ingeniería en Datos e Inteligencia Organizacional
Universidad del Caribe

**Eduardo Mauricio Garrido Rodriguez**
Ingeniería en Datos e Inteligencia Organizacional
Universidad del Carine
---

## 📄 Licencia

Proyecto académico con fines educativos.

```
