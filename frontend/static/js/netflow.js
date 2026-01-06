/* ============================================================
    NETFLOW.JS
    Visualización de tráfico de red (NetFlow - Frontend)
    ------------------------------------------------------------
    - Consume métricas agregadas desde /api/traffic
    - Muestra:
        • Tráfico total
        • Top IPs por consumo
        • Top protocolos
    - NO captura tráfico real desde el navegador
============================================================ */

/* ============================================================
    VARIABLES GLOBALES
============================================================ */

// Gráfica de barras: consumo por IP
let ipChart = null;

// Gráfica de dona: consumo por protocolo
let protoChart = null;

/* ============================================================
    FUNCIÓN PRINCIPAL NETFLOW
    Se ejecuta cada 2 segundos
============================================================ */
async function loadNetflow() {
    try {
        // Solicitud al backend con métricas de tráfico
        const res = await fetch("/api/traffic");
        const data = await res.json();

        /* ====================================================
            TOTAL DE TRÁFICO
        ==================================================== */
        // Muestra el total agregado de tráfico (MB)
        document.getElementById("total-traffic").innerText =
            `${data.total_mb} MB`;

        /* ====================================================
            TOP IPs POR CONSUMO
        ==================================================== */
        // Etiquetas: direcciones IP
        const ipLabels = data.ips.map(i => i.ip);

        // Valores bytes → KB (solo para visualización)
        const ipValues = data.ips.map(i => (i.bytes / 1024).toFixed(2));

        // Crear gráfica solo la primera vez
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
                    plugins: 
                    {
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
            // Actualizar datos sin recrear la gráfica
            ipChart.data.labels = ipLabels;
            ipChart.data.datasets[0].data = ipValues;
            ipChart.update();
        }

        /* ====================================================
            TOP PROTOCOLOS
        ==================================================== */
        // Etiquetas: nombre del protocolo
        const protoLabels = data.protocols.map(p => p.name);

        // Valores: byte → KB
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
        // Error de red o backend
        console.error("Error NetFlow:", err);
    }
}

/* ============================================================
    AUTO-REFRESH
============================================================ */

// Actualiza métricas cada 2 segundos
setInterval(loadNetflow, 2000);
// Primera carga al abrir la página
document.addEventListener("DOMContentLoaded", loadNetflow);

