// frontend/static/js/grouping.js
// =================================
// Asignación visual IP → grupo
// =================================

function getGroupForIP(ip) {
    for (const group of NETWORK_GROUPS) {
        if (!group.segment) continue;

        // Heurística simple: primeros dos octetos
    const base = group.segment.split(".").slice(0, 2).join(".");
    if (ip.startsWith(base + ".")) {
        return group;
    } 
}

    // Default
    return NETWORK_GROUPS.find(g => g.segment === null);
}
