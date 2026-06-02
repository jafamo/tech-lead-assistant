# 001 — Bootstrap & Infraestructura

**Prioridad**: 1 (fundación — todo lo demás depende de esto)
**Rama**: `feature/001-bootstrap`

## Descripción

Configuración inicial de la aplicación: carga de `.env`, inicialización de la base de datos SQLite, creación de la estructura de `data_root` en el primer arranque, y flujo de onboarding (Flow A de la spec).

## Requisitos funcionales

### Configuración
- Todas las rutas (`TLA_DATA_ROOT`, `TLA_DB_PATH`, `TLA_STATS_DIR`, `TLA_REPORTS_IMPORT_DIR`, `TLA_LOG_DIR`) se cargan desde `.env` vía `config.py`.
- Valores por defecto por SO si no se especifican.
- `TLA_DB_PATH` siempre local; las demás pueden ser red (SMB/NFS).

### Primer arranque (Flow A)
- Detectar que no existe cuenta de usuario → mostrar wizard de primer arranque.
- Wizard: crear username + password, confirmar o elegir `TLA_DATA_ROOT`.
- Mostrar banner de recomendación de Full Disk Encryption del SO.
- Crear en `data_root` si no existen: `AGENTS.md`, `README.md`, `templates/`, `_published_schema/`, `_import/`, `_stats/current/`, `_stats/history/`, `_archive/`, `_shared/meetings/`.
- Publicar `content.schema.json` en `_published_schema/`.
- Mostrar pantalla Inicio con tabla vacía + mensaje de onboarding.

### Inicialización de la base de datos
- Crear/migrar schema SQLite al arrancar (tablas: `user`, `team_member`, `meeting_type`, `meeting`, `meeting_participant`, `report`, `report_meeting`, `scheduled_meeting`, `search_index` FTS5).
- Poblar `meeting_type` con los tipos por defecto: `oneToOne`, `seguimiento`, `feedback`, `tecnica`, `retro`.

### Observabilidad
- Logs locales con rotación en `TLA_LOG_DIR`.
- Nivel configurable con `TLA_LOG_LEVEL`.

## Requisitos no funcionales

- Arranque < 3 s en local, < 10 s en red.
- Estado "desconectado" sin crash si `data_root` está en red y cae.
- Cross-platform: Windows 10+, Ubuntu 22.04+, Fedora 38+.
