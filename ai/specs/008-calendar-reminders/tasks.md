# 008 — Calendario y Recordatorios: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Entidad `ScheduledMeeting` (miembro, tipo, fecha, hora, duración, recurrencia, status)
- [ ] Use case `ScheduleMeeting` — crea reunión programada, expande recurrencias
- [ ] Use case `MarkMeetingCompleted` — actualiza status, ofrece match con transcripción subida
- [ ] Use case `CancelMeeting` — registra `cancelled_at`
- [ ] Use case `ListUpcomingMeetings` — por miembro o global, próximas N semanas
- [ ] Use case `ExportMeetingsToICS` — exporta rango de reuniones a `.ics`
- [ ] Port `CalendarRepository` — interfaz CRUD
- [ ] Port `ICSExporterPort` — interfaz exportación .ics
- [ ] Tests unitarios de todos los use cases

## Adapters

- [ ] `adapters/db/calendar_repo.py` — implementa `CalendarRepository`
- [ ] `adapters/exporters/ics.py` — genera `.ics` con `icalendar` library
- [ ] Lógica de expansión de recurrencia (semanal, bi-semanal, mensual)

## UI

- [ ] Widget de próximas reuniones en vista de detalle de miembro
- [ ] Modal "Programar reunión": tipo, fecha, hora, duración, recurrencia
- [ ] Lista de próximas reuniones en Inicio (integrado con componente existente)
- [ ] Botón "Marcar completada" con sugerencia de match de transcripción
- [ ] Botón "Exportar a .ics" (reunión individual o rango)

## Tests

- [ ] Test unitario: `ScheduleMeeting` — recurrencias expandidas correctamente
- [ ] Test unitario: `MarkMeetingCompleted`
- [ ] Test unitario: `ExportMeetingsToICS` — `.ics` válido
- [ ] Test integración: `CalendarRepository` contra SQLite en memoria
