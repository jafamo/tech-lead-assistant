# 008 — Calendario Interno y Recordatorios

**Prioridad**: 8
**Rama**: `feature/008-calendar-reminders`
**Depende de**: 003-team-management, 007-home-navigation

## Descripción

Calendario interno de reuniones programadas, recurrencia, marcado de completadas y exportación a `.ics` para importar en Google Calendar / Outlook.

## Requisitos funcionales

Extraídos de §6.10 de la spec:

### Gestión de reuniones programadas
- **RF-CAL-1**: Crear reunión programada para un miembro (tipo, título, fecha, hora, duración).
- **RF-CAL-2**: Soporte de recurrencia: semanal, bi-semanal, mensual. Con fecha de fin opcional.
- **RF-CAL-3**: Marcar reunión como completada (idealmente al subir la transcripción correspondiente — la app ofrece el match automático).
- **RF-CAL-4**: Cancelar reunión con registro (`cancelled_at`).
- **RF-CAL-5**: Exportar reunión individual o rango de fechas a `.ics` para importar en Google Calendar / Outlook.
- **RF-CAL-6**: Vista de próximas reuniones: en la vista de detalle del miembro y en Inicio.

### Integración con el banner de alertas
- Reuniones de esta semana → alerta 🗓️ en el banner.
- Reuniones vencidas (pasadas, status `pending`) → alerta ⚠️ en el banner.
- Subir transcripción → ofrecer marcar la reunión programada correspondiente como completada.

## Schema de datos

Ver tabla `scheduled_meeting` en §5 de la spec principal. Campos clave:
- `scheduled_date`, `scheduled_time`, `duration_minutes`
- `recurrence` (`weekly` | `biweekly` | `monthly` | NULL)
- `recurrence_end_date`
- `status` (`pending` | `completed` | `cancelled`)

## Casos de uso relacionados

- UC7: Ver banner de reuniones pendientes esta semana.
- UC8: Registrar próxima 1:1 y exportar a `.ics`.

## Notas

- v1 no integra API externa de calendario. Solo exporta `.ics`.
- La integración con Google Calendar / Outlook via OAuth queda para v1.x.
