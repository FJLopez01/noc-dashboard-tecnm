/* static/js/dashboard.js - VERSIÓN FINAL CON SERVICIOS (PUERTOS) */

let myChart = null;

async function update() {
    try {
        const res = await fetch('/api/status');
        const rawData = await res.json(); // Datos crudos
        
        // --- LÓGICA DE BÚSQUEDA ---
        const searchInput = document.getElementById('searchInput');
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';

        const data = rawData.filter(host => {
            const ip = host.ip_address.toLowerCase();
            const name = (host.host_name || '').toLowerCase();
            return ip.includes(searchTerm) || name.includes(searchTerm);
        });

        // Contadores
        const total = rawData.length; 
        const online = rawData.filter(host => host.status === 'online').length;
        const offline = total - online;

        document.getElementById('total-count').innerText = total;
        document.getElementById('online-count').innerText = online;
        document.getElementById('offline-count').innerText = offline;

        const grid = document.getElementById('grid');
        grid.innerHTML = ''; 

        // Si no hay resultados
        if (data.length === 0) {
            grid.innerHTML = `
                <div class="col-12 text-center py-5 opacity-50">
                    <i class="fa-solid fa-magnifying-glass fa-3x mb-3"></i>
                    <h4>No se encontraron hosts</h4>
                    <p>Intenta con otra IP o nombre</p>
                </div>`;
        }

        data.forEach(host => {
            // 1. Estilos y Estados Básicos
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

            // 2. LÓGICA DE UPTIME
            let uptimeVal = host.uptime_percent ? host.uptime_percent.toFixed(1) : '100.0';
            let uptimeClass = 'uptime-high'; 
            if (uptimeVal < 80) uptimeClass = 'uptime-low';
            else if (uptimeVal < 95) uptimeClass = 'uptime-med';

            // --- 3. LÓGICA DE SERVICIOS (NUEVO: PUERTOS) ---
            let servicesHtml = '';
            // Verificamos si trae servicios y si no está vacío
            if (host.services && host.services.length > 0) {
                const servicesList = host.services.split('|');
                
                servicesHtml = '<div class="d-flex gap-2 mt-3 flex-wrap">';
                servicesList.forEach(srv => {
                    const [port, state] = srv.split(':');
                    
                    // Estilos según estado
                    let badgeColor = state === 'OPEN' ? 'bg-primary' : 'bg-secondary opacity-25';
                    let iconClass = state === 'OPEN' ? 'fa-check' : 'fa-xmark';
                    
                    // Traducción de puertos a nombres
                    let portName = port;
                    if(port === '80') portName = 'HTTP';
                    if(port === '443') portName = 'HTTPS';
                    if(port === '22') portName = 'SSH';
                    if(port === '3306') portName = 'SQL';
                    if(port === '53') portName = 'DNS';
                    if(port === '5000') portName = 'API';

                    servicesHtml += `
                        <span class="badge ${badgeColor} bg-opacity-25 border border-primary border-opacity-25 text-white px-2 py-1" style="font-size: 0.65rem;">
                            <i class="fa-solid ${iconClass} me-1"></i> ${portName}
                        </span>
                    `;
                });
                servicesHtml += '</div>';
            }
            // -----------------------------------------------

            // 4. Generar Tarjeta HTML
            const cardHTML = `
                <div class="col-xl-3 col-lg-4 col-md-6">
                    <div class="card glass-card h-100 p-3" onclick="loadHistory('${host.ip_address}')">
                        
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

            if (searchTerm === '') {
                addLogToConsole(host, displayName);
            }
        });

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// --- FUNCIÓN CONSOLA WIRESHARK ---
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
    if (consoleDiv.children.length > 50) {
        consoleDiv.lastElementChild.remove();
    }
}

// --- FUNCIÓN GRÁFICAS ---
async function loadHistory(ip) {
    const modal = new bootstrap.Modal(document.getElementById('historyModal'));
    document.getElementById('modalTitle').innerHTML = `<i class="fa-solid fa-chart-line me-2 text-primary"></i> Historial: ${ip}`;
    modal.show();

    const res = await fetch(`/api/history/${ip}`);
    const historyData = await res.json();

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
                tension: 0.4,
                fill: true,
                backgroundColor: gradient
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8', maxTicksLimit: 6 } }
            }
        }
    });
}

setInterval(update, 3000);
update();