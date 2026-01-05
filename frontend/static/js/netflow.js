let ipChart = null;
let protoChart = null;

async function loadNetflow() {
    try {
        const res = await fetch("/api/traffic");
        const data = await res.json();

        // ---------- TOTAL TRAFFIC ----------
        document.getElementById("total-traffic").innerText =
            `${data.total_mb} MB`;

        // ---------- TOP IPs ----------
        const ipLabels = data.ips.map(i => i.ip);
        const ipValues = data.ips.map(i => (i.bytes / 1024).toFixed(2));

        if (!ipChart) {
            ipChart = new Chart(document.getElementById("ipChart"), {
                type: "bar",
                data: {
                    labels: ipLabels,
                    datasets: [{
                        label: "KB transferidos",
                        data: ipValues,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            ipChart.data.labels = ipLabels;
            ipChart.data.datasets[0].data = ipValues;
            ipChart.update();
        }

        // ---------- TOP PROTOCOLS ----------
        const protoLabels = data.protocols.map(p => p.name);
        const protoValues = data.protocols.map(p => (p.bytes / 1024).toFixed(2));

        if (!protoChart) {
            protoChart = new Chart(document.getElementById("protoChart"), {
                type: "doughnut",
                data: {
                    labels: protoLabels,
                    datasets: [{
                        data: protoValues
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: "bottom",
                            labels: {
                                boxWidth: 12
                            }
                        }
                    }
                }
            });
        } else {
            protoChart.data.labels = protoLabels;
            protoChart.data.datasets[0].data = protoValues;
            protoChart.update();
        }

    } catch (err) {
        console.error("Error NetFlow:", err);
    }
}

// ---------- REFRESH ----------
setInterval(loadNetflow, 2000);
document.addEventListener("DOMContentLoaded", loadNetflow);

