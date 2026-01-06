// Estructura visual de agrupación (NO lógica)
const NETWORK_GROUPS = [
  {
    name: "Administración",
    segment: "192.168.1.0/24",
    description: "Oficinas administrativas",
    color: "primary"
  },
  {
    name: "Laboratorios",
    segment: "192.168.2.0/24",
    description: "Aulas de cómputo",
    color: "success"
  },
  {
    name: "Biblioteca",
    segment: "192.168.3.0/24",
    description: "Área de consulta",
    color: "warning"
  },
  {
    name: "Sin clasificar",
    segment: null,
    description: "Equipos fuera de segmentos definidos",
    color: "secondary"
  }
];
