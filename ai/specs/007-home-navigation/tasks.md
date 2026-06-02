# 007 — Inicio y Navegación: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Use case `GetHomeDashboard` — agrega datos para la tabla del personal (última reunión, próxima reunión, AI open count, último report)
- [ ] Use case `GetPendingAlerts` — calcula todas las alertas del banner
- [ ] Tests unitarios de todos los use cases

## UI

- [ ] `adapters/ui/layout/sidebar.py` — sidebar con navegación, badge de alertas, colapsable
- [ ] `adapters/ui/layout/topbar.py` — barra superior con título de página y usuario
- [ ] `adapters/ui/pages/home.py` — página Inicio
- [ ] `adapters/ui/components/banner_alerts.py` — banner de alertas clickeables
- [ ] `adapters/ui/components/personnel_table.py` — tabla del personal
  - [ ] Columna color dot (usa color del miembro)
  - [ ] Columna última reunión (rojo si > 3 semanas)
  - [ ] Columna próxima reunión (verde / rojo según estado)
  - [ ] Columna action items open (badge naranja/rojo)
  - [ ] Columna último report (periodo + modo icono + fecha)
  - [ ] Columna acciones (Generar / Importar / Ver / Exportar)
- [ ] Buscador rápido sobre la tabla
- [ ] Link "Ver archivados (N)" bajo la tabla
- [ ] `adapters/ui/components/action_buttons.py` — botones reutilizables con iconos y tooltips

## Integración de alertas

- [ ] Alerta: reuniones esta semana (de `scheduled_meeting`)
- [ ] Alerta: reuniones vencidas
- [ ] Alerta: action items abiertos > 30 días
- [ ] Alerta: temas recurrentes en ≥ 3 reports recientes
- [ ] Alerta: miembros sin reunión > 3 semanas
- [ ] Alerta: reports en staging dir pendientes de importar
- [ ] Alerta: `data_root` desconectado

## Tests

- [ ] Test unitario: `GetPendingAlerts` — cada tipo de alerta por separado
- [ ] Test unitario: `GetHomeDashboard` — agrupación y ordenación
