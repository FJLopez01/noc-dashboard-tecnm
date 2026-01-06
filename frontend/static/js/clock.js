/* ============================================================
    CLOCK.JS
    Reloj en tiempo real para el dashboard
    ------------------------------------------------------------
    - Muestra fecha y hora actual
    - Actualización cada segundo
    - Función puramente visual (frontend)
============================================================ */

/* ============================================================
    FUNCIÓN PRINCIPAL DEL RELOJ
============================================================ */
function startClock() {

    // Elemento HTML donde se mostrará el reloj
    const clockElement = document.getElementById('live-clock');

    /* --------------------------------------------------------
        ACTUALIZA FECHA Y HORA
    -------------------------------------------------------- */
    function updateTime() {
        // Fecha y hora actual del navegador
        const now = new Date();

        // Hora en formato 24h → 14:30:45
        const timeString = now.toLocaleTimeString('es-MX', {
            hour12: false
        });

        // Fecha corta → jue, 21 nov
        const dateString = now.toLocaleDateString('es-MX', {
            weekday: 'short',
            day: 'numeric',
            month: 'short'
        });

        // Render dinámico con ícono
        clockElement.innerHTML = `
            <i class="fa-regular fa-clock me-2 text-primary"></i>
            ${dateString} • ${timeString}
        `;
    }

    /* --------------------------------------------------------
        TIMER
    -------------------------------------------------------- */
    // Actualizar cada segundo
    setInterval(updateTime, 1000);

    // Ejecutar inmediatamente al cargar
    updateTime();
}

/* ============================================================
    INICIALIZACIÓN
============================================================ */
document.addEventListener('DOMContentLoaded', startClock);
