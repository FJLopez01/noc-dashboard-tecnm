/* ============================================================
    DASHBOARD.JS
    Lógica principal del Frontend del NOC Dashboard
    ------------------------------------------------------------
    - Consume APIs del backend
    - Renderiza tarjetas de hosts
    - Maneja búsqueda, KPIs, consola y gráficas
   ============================================================ */

/* ============================================================
    VARIABLES GLOBALES
    ============================================================ */

// Referencia a la gráfica de historial (Chart.js)
let myChart = null;

// Guarda el último estado recibido para evitar renders innecesarios
let lastDataString = null;


/* ============================================================
    FUNCIÓN PRINCIPAL DE ACTUALIZACIÓN
    Se ejecuta cada 3 segundos
    ============================================================ */
async function update() {
    try {
        // Petición al backend con el estado actual de la red
        const res = await fetch('/api/status');
        
        // Validación HTTP básica
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        // Datos crudos del backend (array de hosts)
        const rawData = await res.json();
        
        /* ====================================================
            LOADER INICIAL
            ==================================================== */
        const loader = document.getElementById('initial-loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 300);
        }
        
        /* ====================================================
            OPTIMIZACIÓN
            Solo redibujar si los datos cambiaron
        ==================================================== */
        const currentDataString = JSON.stringify(rawData);
        if (currentDataString === lastDataString) {
            return; // No hay cambios → no renderiza
        }
        lastDataString = currentDataString;
        
        /* ====================================================
            BÚSQUEDA EN TIEMPO REAL
            ==================================================== */
        const searchInput = document.getElementById('searchInput');
        const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';

        // Filtrar hosts por IP o nombre
        const data = rawData.filter(host => {
            const ip = host.ip_address.toLowerCase();
            const name = (host.host_name || '').toLowerCase();
            return ip.includes(searchTerm) || name.includes(searchTerm);
        });


        /* ====================================================
            KPIs (NO dependen del filtro)
            ==================================================== */
        const total = rawData.length; 
        const online = rawData.filter(host => host.status === 'online').length;
        const offline = total - online;

        // Animación de números
        animateNumber('total-count', total);
        animateNumber('online-count', online);
        animateNumber('offline-count', offline);


        /* ====================================================
            GRID DE HOSTS
            ==================================================== */
        const grid = document.getElementById('grid');
        grid.innerHTML = ''; 

        // Caso si no hay resultados de búsqueda
        if (data.length === 0) {
            grid.innerHTML = `
                <div class="col-12 text-center py-5 opacity-50" style="animation: fadeIn 0.5s ease-out;">
                    <i class="fa-solid fa-magnifying-glass fa-3x mb-3 text-primary"></i>
                    <h4 class="text-white">No se encontraron hosts</h4>
                    <p class="text-white-50">Intenta con otra IP o nombre</p>
                    ${searchTerm ? `<button class="btn btn-sm btn-outline-primary mt-2" onclick="document.getElementById('searchInput').value=''; update();">
                        <i class="fa-solid fa-times me-1"></i> Limpiar búsqueda
                    </button>` : ''}
                </div>`;
            return;
        }


        /* ====================================================
            RENDER DE CADA HOST
            ==================================================== */
        data.forEach(host => {
            

            /* -----------------------------------------------
                ESTADO Y LATENCIA
                ----------------------------------------------- */
            let statusClass = 'status-offline';
            let statusText = 'OFFLINE';
            let icon = '<i class="fa-solid fa-triangle-exclamation text-danger fa-2x"></i>';
            let latencyHtml = '<span class="text-muted">--</span>';

            let displayName = host.host_name || host.ip_address;

            if (host.status === 'online') {
                statusText = 'ONLINE';
                icon = '<i class="fa-solid fa-server text-primary fa-2x"></i>';
                
                let latencyColor = 'text-white';
                if (host.latency_ms < 100) {
                    statusClass = 'status-online';
                } else if (host.latency_ms < 300) {
                    statusClass = 'status-warning';
                    latencyColor = 'text-warning';
                    icon = '<i class="fa-solid fa-wifi text-warning fa-2x"></i>';
                } else {
                    statusClass = 'status-offline';
                    latencyColor = 'text-danger';
                    icon = '<i class="fa-solid fa-gauge-high text-danger fa-2x"></i>';
                }
                
                latencyHtml = `<span class="fs-3 fw-bold ${latencyColor}">${host.latency_ms}</span> <span class="text-secondary fs-6">ms</span>`;
            }


            /* -----------------------------------------------
                UPTIME
                ----------------------------------------------- */
            let uptimeVal = host.uptime_percent ? host.uptime_percent.toFixed(1) : '100.0';
            let uptimeClass = 'uptime-high'; 
            if (uptimeVal < 80) uptimeClass = 'uptime-low';
            else if (uptimeVal < 95) uptimeClass = 'uptime-med';


            /* -----------------------------------------------
                SERVICIOS / PUERTOS
                ----------------------------------------------- */
            let servicesHtml = '';


            if (host.services && host.services.length > 0) {
                const servicesList = host.services.split('|');
                
                servicesHtml = '<div class="d-flex gap-2 mt-3 flex-wrap">';
                servicesList.forEach(srv => {
                    const [port, state] = srv.split(':');
                    
                    let badgeColor = state === 'OPEN' ? 'bg-primary' : 'bg-secondary opacity-25';
                    let iconClass = state === 'OPEN' ? 'fa-check' : 'fa-xmark';
                    
                    // Traducción de puertos a nombres
                    let portName = port;
                    const portMap = {
                        '80': 'HTTP', '443': 'HTTPS', '22': 'SSH',
                        '3306': 'MySQL', '53': 'DNS', '5000': 'API',
                        '21': 'FTP', '25': 'SMTP', '3389': 'RDP',
                        '5432': 'PostgreSQL', '8080': 'HTTP-ALT'
                    };
                    portName = portMap[port] || `Port ${port}`;

                    servicesHtml += `
                        <span class="badge ${badgeColor} bg-opacity-25 border border-primary border-opacity-25 text-white px-2 py-1" style="font-size: 0.65rem;" title="Puerto ${port}: ${state}">
                            <i class="fa-solid ${iconClass} me-1"></i> ${portName}
                        </span>
                    `;
                });
                servicesHtml += '</div>';
            }

            /* -----------------------------------------------
                TARJETA FINAL
                ----------------------------------------------- */
            const cardHTML = `
                <div class="col-xl-3 col-lg-4 col-md-6">
                    <div class="card glass-card h-100 p-3" onclick="loadHistory('${host.ip_address}')" title="Click para ver historial">
                        
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div class="d-flex align-items-center">
                                <div class="${statusClass} status-indicator"></div>
                                <span class="fw-bold text-white-50 small text-uppercase" style="letter-spacing: 1px;">${statusText}</span>
                            </div>
                            ${icon}
                        </div>
                        
                        <h5 class="fw-bold mb-0 text-white text-truncate" title="${displayName}">${displayName}</h5>
                        <small class="text-secondary font-monospace opacity-75">${host.ip_address}</small>
                        
                        ${servicesHtml}

                        <div class="mt-3 pt-3 border-top border-secondary border-opacity-10 d-flex align-items-end justify-content-between">
                            
                            <div>
                                <p class="mb-0 text-secondary small text-uppercase" style="font-size: 0.65rem;">Latencia</p>
                                ${latencyHtml}
                            </div>

                            <div class="text-end">
                                <p class="mb-1 text-secondary small text-uppercase" style="font-size: 0.65rem;">Disponibilidad</p>
                                <div class="uptime-badge">
                                    <i class="fa-solid fa-chart-pie ${uptimeClass}"></i>
                                    <span class="${uptimeClass}">${uptimeVal}%</span>
                                </div>
                                <div class="mt-1">
                                    <small class="text-white-50" style="font-size: 0.65rem;">Act: ${new Date(host.timestamp).toLocaleTimeString()}</small>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            `;
            grid.innerHTML += cardHTML;

            // Agregar log a consola solo si NO hay búsqueda activa
            if (searchTerm === '') {
                addLogToConsole(host, displayName);
            }

            renderGroups(rawData);

        });

    } catch (error) {
        console.error('Error fetching data:', error);
        
        // Mostrar error visual en el grid
        const grid = document.getElementById('grid');
        grid.innerHTML = `
            <div class="col-12 text-center py-5" style="animation: fadeIn 0.5s ease-out;">
                <i class="fa-solid fa-triangle-exclamation text-danger fa-3x mb-3"></i>
                <h4 class="text-danger">Error de Conexión</h4>
                <p class="text-white-50">No se pudo conectar con el servidor de monitoreo</p>
                <small class="text-secondary d-block mb-3">Error: ${error.message}</small>
                <button class="btn btn-primary" onclick="update()">
                    <i class="fa-solid fa-rotate-right me-2"></i> Reintentar
                </button>
            </div>
        `;
    }
}


/* ============================================================
    ANIMACIÓN DE KPIs
    ============================================================ */
function animateNumber(elementId, targetValue) {
    const element = document.getElementById(elementId);
    const currentValue = parseInt(element.innerText) || 0;
    
    if (currentValue === targetValue) return;
    
    const duration = 500; // ms
    const steps = 20;
    const stepValue = (targetValue - currentValue) / steps;
    const stepDuration = duration / steps;
    
    let currentStep = 0;
    const interval = setInterval(() => {
        currentStep++;
        const newValue = Math.round(currentValue + (stepValue * currentStep));
        element.innerText = newValue;
        
        if (currentStep >= steps) {
            element.innerText = targetValue;
            clearInterval(interval);
        }
    }, stepDuration);
}

/* ============================================================
    CONSOLA TIPO WIRESHARK (VISUAL)
    ============================================================ */
function addLogToConsole(host, name) {
    const consoleDiv = document.getElementById('live-console');
    if (!consoleDiv) return; 

    const now = new Date().toLocaleTimeString('es-MX', { hour12: false });
    
    let logClass = 'log-success';
    let info = `SEQ=1 TTL=64 TIME=${host.latency_ms}ms`;
    
    if (host.status !== 'online') {
        logClass = 'log-error';
        info = `DESTINATION HOST UNREACHABLE / TIMEOUT`;
    } else if (host.latency_ms > 100) {
        logClass = 'log-warning';
    }

    const logHTML = `
        <div class="log-entry ${logClass}">
            <div>
                <span class="log-timestamp">[${now}]</span>
                <span class="log-protocol">ICMP</span>
                <span class="me-2 fw-bold">${name}</span>
                <span class="opacity-50 small">(${host.ip_address})</span>
                <span>&rarr; SERVER</span>
            </div>
            <div class="font-monospace small opacity-75">
                ${info}
            </div>
        </div>
    `;

    consoleDiv.insertAdjacentHTML('afterbegin', logHTML);
    
    // Mantener solo los últimos 50 logs
    while (consoleDiv.children.length > 50) {
        consoleDiv.lastElementChild.remove();
    }
}

// --- LIMPIAR CONSOLA ---
function clearConsole() {
    const consoleDiv = document.getElementById('live-console');
    if (consoleDiv) {
        consoleDiv.innerHTML = '<div class="text-center text-secondary py-3"><i>Consola limpiada</i></div>';
    }
}

/* ============================================================
    HISTORIAL DE LATENCIA (MODAL + CHART.JS)
    ============================================================ */
async function loadHistory(ip) {
    const modal = new bootstrap.Modal(document.getElementById('historyModal'));
    document.getElementById('modalTitle').innerHTML = `<i class="fa-solid fa-chart-line me-2 text-primary"></i> Historial: ${ip}`;
    modal.show();

    try {
        const res = await fetch(`/api/history/${ip}`);
        const historyData = await res.json();

        if (historyData.length === 0) {
            document.getElementById('historyChart').parentElement.innerHTML = `
                <div class="text-center py-5">
                    <i class="fa-solid fa-database text-secondary fa-3x mb-3"></i>
                    <p class="text-white-50">No hay datos históricos disponibles para esta IP</p>
                </div>
            `;
            return;
        }

        const labels = historyData.map(d => new Date(d.timestamp).toLocaleTimeString());
        const points = historyData.map(d => d.latency_ms);

        if (myChart) myChart.destroy();

        const ctx = document.getElementById('historyChart').getContext('2d');
        let gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(56, 189, 248, 0.5)');
        gradient.addColorStop(1, 'rgba(56, 189, 248, 0.0)');

        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Latencia (ms)',
                    data: points,
                    borderColor: '#38bdf8',
                    borderWidth: 3,
                    pointBackgroundColor: '#0f172a',
                    pointBorderColor: '#38bdf8',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    tension: 0.4,
                    fill: true,
                    backgroundColor: gradient
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(56, 189, 248, 0.5)',
                        borderWidth: 2,
                        padding: 12,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return `Latencia: ${context.parsed.y} ms`;
                            }
                        }
                    }
                },
                scales: {
                    y: { 
                        beginAtZero: true, 
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }, 
                        ticks: { color: '#94a3b8' },
                        title: { display: true, text: 'Latencia (ms)', color: '#94a3b8' }
                    },
                    x: { 
                        grid: { display: false }, 
                        ticks: { color: '#94a3b8', maxTicksLimit: 8 },
                        title: { display: true, text: 'Tiempo', color: '#94a3b8' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error cargando historial:', error);
        document.getElementById('historyChart').parentElement.innerHTML = `
            <div class="text-center py-5">
                <i class="fa-solid fa-triangle-exclamation text-danger fa-3x mb-3"></i>
                <p class="text-danger">Error al cargar el historial</p>
            </div>
        `;
    }
}

/* ============================================================
    EVENTOS Y AUTO-REFRESH
    ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            update();
        });
    }
    
    // Botón de limpiar consola
    const clearBtn = document.getElementById('clearConsole');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearConsole);
    }
});

/* ============================================================
    GESTION DE SEGMENTOS
    ============================================================ */
async function saveSegment() {
    const input = document.getElementById("segmentInput");
    if (!input) return;

    const segment = input.value.trim();
    if (!segment) return;

    const res = await fetch("/api/segments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ segment })
    });

    if (res.ok) {
        input.value = "";
        loadSegments();
        alert("Segmento añadido correctamente");
    } else {
        alert("Segmento inválido");
    }
}

async function loadSegments() {
    const res = await fetch("/api/segments");
    const segments = await res.json();

    const list = document.getElementById("segmentList");
    list.innerHTML = "";

    segments.forEach(seg => {
        list.innerHTML += `
            <li class="list-group-item d-flex justify-content-between align-items-center bg-transparent text-white">
                <span class="font-monospace">${seg}</span>
                <button class="btn btn-sm btn-outline-danger"
                        onclick="deleteSegment('${seg}')">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </li>
        `;
    });
}

async function deleteSegment(segment) {
    if (!confirm(`¿Eliminar el segmento ${segment}?`)) return;

    const res = await fetch(`/api/segments/${encodeURIComponent(segment)}`, {
    method: "DELETE"
    });

    if (res.ok) {
        loadSegments();
    } else {
        alert("No se pudo eliminar el segmento");
    }
}

/* =========================================
    AGRUPACIÓN VISUAL POR SEGMENTO (MOCKUP)
    NO impacta backend
========================================= */

function groupHostsBySegment(hosts) {
    const groups = {};

    hosts.forEach(host => {
        const ip = host.ip_address || "0.0.0.0";
        const segment = ip.split(".").slice(0, 3).join(".") + ".0/24";

        if (!groups[segment]) {
            groups[segment] = [];
        }
        groups[segment].push(host);
    });

    return groups;
}

function renderGroups(hosts) {
    const container = document.getElementById("groups-container");
    if (!container) return;

    container.innerHTML = "";

    const groups = groupHostsBySegment(hosts);

    Object.entries(groups).forEach(([segment, hosts]) => {
        const online = hosts.filter(h => h.status === "online").length;

        const card = document.createElement("div");
        card.className = "glass-card segment-card p-4 mb-4";

        card.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0 text-info">
                    <i class="fa-solid fa-network-wired me-2"></i>
                    Segmento ${segment}
                </h5>
                <span class="badge bg-primary bg-opacity-25">
                    ${online}/${hosts.length} online
                </span>
            </div>

            <div class="row g-3">
                ${hosts.map(h => `
                    <div class="col-md-4">
                        <div class="p-3 rounded bg-dark bg-opacity-50">
                            <strong>${h.host_name || h.ip_address}</strong><br>
                            <small class="text-secondary">${h.ip_address}</small><br>
                            <span class="badge ${
                                h.status === "online" ? "bg-success" : "bg-danger"
                            } mt-2">
                                ${h.status}
                            </span>
                        </div>
                    </div>
                `).join("")}
            </div>
        `;

    container.appendChild(card);
});
}


document.getElementById("segmentModal")
    .addEventListener("shown.bs.modal", loadSegments);


// Actualizar cada 3 segundos
setInterval(update, 3000);
update();