let myChart = null;

async function update() {
    try {
        // 1. Pedimos los datos al backend
        const res = await fetch('/api/status');
        const data = await res.json();
        
        // --- LÓGICA MATEMÁTICA (NUEVO) ---
        // Calculamos los números para la barra superior
        const total = data.length;
        const online = data.filter(host => host.status === 'online').length;
        const offline = total - online;

        // Actualizamos los números en el HTML
        document.getElementById('total-count').innerText = total;
        document.getElementById('online-count').innerText = online;
        document.getElementById('offline-count').innerText = offline;
        // ----------------------------------

        const grid = document.getElementById('grid');
        grid.innerHTML = ''; // Limpiamos el grid para volver a dibujar

        data.forEach(host => {
            // 2. Determinar estado y estilos visuales
            let statusClass = 'status-offline';
            let statusText = 'OFFLINE';
            let icon = '<i class="fa-solid fa-triangle-exclamation text-danger fa-2x"></i>';
            let latencyHtml = '<span class="text-muted">--</span>';

            if (host.status === 'online') {
                statusText = 'ONLINE';
                icon = '<i class="fa-solid fa-server text-primary fa-2x"></i>';
                
                // Lógica de Latencia (Colores)
                let latencyColor = 'text-white';
                if (host.latency_ms < 100) {
                    statusClass = 'status-online'; // Verde
                } else if (host.latency_ms < 300) {
                    statusClass = 'status-warning'; // Amarillo
                    latencyColor = 'text-warning';
                    icon = '<i class="fa-solid fa-wifi text-warning fa-2x"></i>';
                } else {
                    statusClass = 'status-offline'; // Rojo (Lento)
                    latencyColor = 'text-danger';
                    icon = '<i class="fa-solid fa-gauge-high text-danger fa-2x"></i>';
                }
                
                latencyHtml = `<span class="fs-3 fw-bold ${latencyColor}">${host.latency_ms}</span> <span class="text-secondary fs-6">ms</span>`;
            }

            // 3. Crear la tarjeta con diseño Glassmorphism
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
                        
                        <h5 class="fw-bold mb-1 text-white">${host.ip_address}</h5>
                        
                        <div class="mt-3 d-flex align-items-end justify-content-between">
                            <div>
                                <p class="mb-0 text-secondary small text-uppercase" style="font-size: 0.7rem;">Latencia</p>
                                ${latencyHtml}
                            </div>
                            <div class="text-end">
                                <p class="mb-0 text-secondary small" style="font-size: 0.7rem;">Actualizado</p>
                                <small class="text-white-50" style="font-size: 0.8rem;">${new Date(host.timestamp).toLocaleTimeString()}</small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            grid.innerHTML += cardHTML;
        });

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Función para cargar gráfica (Estilo mejorado)
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
    
    // Gradiente para la gráfica (Azul Ciberpunk)
    let gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(56, 189, 248, 0.5)'); // Azul claro arriba
    gradient.addColorStop(1, 'rgba(56, 189, 248, 0.0)'); // Transparente abajo

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Latencia (ms)',
                data: points,
                borderColor: '#38bdf8', // Azul Cian
                borderWidth: 3,
                pointBackgroundColor: '#0f172a',
                pointBorderColor: '#38bdf8',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                tension: 0.4, // Curva suave
                fill: true,
                backgroundColor: gradient
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: 10,
                    displayColors: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8', maxTicksLimit: 6 }
                }
            }
        }
    });
}

// Actualizar cada 3 segundos
setInterval(update, 3000);
update();