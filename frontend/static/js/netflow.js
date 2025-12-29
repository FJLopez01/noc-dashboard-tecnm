/* static/js/netflow.js */

let ipChart = null;
let protoChart = null;

async function updateNetflow() {
    try {
        const res = await fetch('/api/netflow/live');
        if (!res.ok) throw new Error('NetFlow API error');

        const data = await res.json();

        // --- TOTAL TRAFFIC ---
        const totalMB = (data.total_bytes / (1024 * 1024)).toFixed(2);
        document.getElementById('total-traffic').innerText = `${totalMB} MB`;

        // --- TOP IPs ---
        const ipLabels = data.top_ips.map(i => i.ip);
        const ipValues = data.top_ips.map(i => (i.bytes / (1024 * 1024)).toFixed(2));

        renderIpChart(ipLabels, ipValues);

        // --- PROTOCOLS ---
        const protoLabels = Object.keys(data.protocols);
        const protoValues = Object.values(data.protocols);

        renderProtoChart(protoLabels, protoValues);

    } catch (err) {
        console.error('NetFlow error:', err);
    }
}

// ------------------ CHARTS ------------------

function renderIpChart(labels, values) {
    const ctx = document.getElementById('ipChart').getContext('2d');

    if (ipChart) ipChart.destroy();

    ipChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Consumo (MB)',
                data: values,
                borderWidth: 1,
                backgroundColor: 'rgba(56, 189, 248, 0.6)',
                borderColor: 'rgba(56, 189, 248, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(255,255,255,0.05)' }
                },
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { display: false }
                }
            }
        }
    });
}

function renderProtoChart(labels, values) {
    const ctx = document.getElementById('protoChart').getContext('2d');

    if (protoChart) protoChart.destroy();

    protoChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    '#38bdf8',
                    '#22c55e',
                    '#f59e0b',
                    '#ef4444'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#e5e7eb' }
                }
            }
        }
    });
}

// --- INTERVAL ---
setInterval(updateNetflow, 2000);
updateNetflow();
