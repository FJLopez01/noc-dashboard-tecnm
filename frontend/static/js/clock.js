function startClock() {
    const clockElement = document.getElementById('live-clock');
    
    function updateTime() {
        const now = new Date();
        // Formato: 14:30:45
        const timeString = now.toLocaleTimeString('es-MX', { hour12: false });
        // Formato fecha: Jueves, 21 Nov
        const dateString = now.toLocaleDateString('es-MX', { weekday: 'short', day: 'numeric', month: 'short' });
        
        clockElement.innerHTML = `<i class="fa-regular fa-clock me-2 text-primary"></i> ${dateString} • ${timeString}`;
    }

    setInterval(updateTime, 1000);
    updateTime(); // Ejecutar inmediatamente
}

document.addEventListener('DOMContentLoaded', startClock);