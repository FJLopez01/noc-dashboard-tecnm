/* static/js/netflow.js */

let ipChart = null;
let protoChart = null;

function initNetFlow() {
    const ctxIp = document.getElementById('ipChart').getContext('2d');
    const ctxProto = document.getElementById('protoChart').getContext('2d');

    // Configuración común para gráficas oscuras
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'right', labels: { color: '#cbd5e1' } }
        },
        scales: {
            y: { ticks: { color: '#94a3b8', beginAtZero: true }, grid: { color: 'rgba(255,255,255,0.05)' } },
            x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
        }
    };

    // Inicializamos gráficas vacías
    ipChart = new Chart(ctxIp, {
        type: 'bar',
        data: { labels: [], datasets: [{ label: 'Bytes', data: [], backgroundColor: '#38bdf8', borderRadius: 4 }] },
        options: commonOptions
    });

    protoChart = new Chart(ctxProto, {
        type: 'doughnut',
        data: { labels: [], datasets: [{ label: 'Bytes', data: [], backgroundColor: ['#f43f5e', '#f59e0b', '#10b981', '#8b5cf6', '#3b82f6'], borderColor: '#0f172a' }] },
        options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { legend: { position: 'right', labels: { color: '#cbd5e1' } } } 
        }
    });

    fetchTrafficData();
    setInterval(fetchTrafficData, 2000); // Actualizar cada 2 seg
}

async function fetchTrafficData() {
    try {
        const res = await fetch('/api/traffic');
        const data = await res.json();

        // Actualizar Texto de Total
        document.getElementById('total-traffic').innerText = data.total_mb + ' MB';

        // Actualizar Gráfica IPs
        ipChart.data.labels = data.ips.map(i => i.ip);
        ipChart.data.datasets[0].data = data.ips.map(i => i.bytes);
        ipChart.update();

        // Actualizar Gráfica Protocolos
        protoChart.data.labels = data.protocols.map(p => p.name);
        protoChart.data.datasets[0].data = data.protocols.map(p => p.bytes);
        protoChart.update();

    } catch (error) {
        console.error("Error NetFlow:", error);
    }
}

document.addEventListener('DOMContentLoaded', initNetFlow);