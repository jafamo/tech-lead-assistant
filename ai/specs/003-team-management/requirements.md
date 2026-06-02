# 003 — Gestión del Equipo

**Prioridad**: 3 (modelo de datos central — todo lo demás referencia miembros)
**Rama**: `feature/003-team-management`
**Depende de**: 001-bootstrap, 002-authentication

## Descripción

CRUD completo de miembros del equipo, incluyendo creación de estructura de directorios, asignación de color, archivado y reactivación.

## Requisitos funcionales

Extraídos de §6.2 de la spec:

- **RF-TEAM-1**: Crear miembro:
  - Formulario: nombre completo, rol.
  - Genera slug (lowercase, sin tildes, espacios → guiones; colisión → sufijo numérico).
  - Asigna color de la paleta (round-robin, editable después).
  - Crea estructura de directorios en `{TLA_DATA_ROOT}/{slug}/`: `profile/`, `oneToOne/`, `seguimiento/`, `feedback/`, `tecnica/`, `retro/`, `notes/`, `reports/`.
  - Crea `profile/profile.md` desde plantilla Jinja2.
  - Registra en `team_member` con `status = active`.
- **RF-TEAM-2**: Renombrar: mueve carpeta al nuevo slug, actualiza índice.
- **RF-TEAM-3 (Archivar)**: Mueve `{TLA_DATA_ROOT}/{slug}/` → `{TLA_DATA_ROOT}/_archive/{slug}/`. Actualiza `status = archived`, registra `archived_at`.
- **RF-TEAM-4 (Reactivar)**: Mueve de vuelta a raíz. `status = active`, limpia `archived_at`.
- **RF-TEAM-5**: Sección "Ver archivados (N)" desde Inicio — tabla con botones "Reactivar" y "Ver historial".
- **RF-TEAM-6**: Cambiar color desde la UI (color picker, paleta de 12).
- **RF-TEAM-7**: Listado con búsqueda por nombre/rol, filtros y ordenación.
- **RF-TEAM-8**: Vista de detalle por persona: timeline de reuniones, color como acento visual, todas las fechas.

## Paleta de colores

12 colores asignados round-robin al crear. Editable por el usuario. El color se usa como acento en toda la UI (dot en tabla, gráficos, barra lateral de detalle).

```
#4A90D9, #E67E22, #27AE60, #8E44AD, #E74C3C,
#1ABC9C, #F39C12, #2980B9, #D35400, #16A085,
#C0392B, #7F8C8D
```

## Casos de uso relacionados

- UC6: Archivar/reactivar miembro.
- UC10: Ver tabla del personal en Inicio.

## Requisitos no funcionales

- Todas las operaciones de filesystem son atómicas (write-temp + rename).
- Archivado y renombrado son reversibles.
- El slug es el identificador permanente — cambiar nombre no rompe historial si el slug no cambia.
