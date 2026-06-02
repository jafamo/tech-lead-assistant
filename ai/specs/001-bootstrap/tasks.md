# 001 — Bootstrap: Tasks

**Estado**: ✅ Completado

## Domain

- [x] Entidad `Config` → `config.py` (pydantic-settings)
- [x] Use case `InitializeDataRoot` — crea la estructura de directorios si no existe
- [x] Use case `PublishSchema` — copia `content.schema.json` a `_published_schema/`
- [x] Port `FileSystemPort` — interfaz para operaciones de FS (mkdir, exists, copy atómica)
- [x] Tests unitarios de `InitializeDataRoot` (FS mockeado)

## Adapters

- [x] `config.py` — carga `.env` con pydantic-settings, resuelve defaults por SO, expone `Settings`
- [x] `adapters/db/models.py` — modelos SQLModel: `User`, `TeamMember`, `MeetingType`, `Meeting`, `MeetingParticipant`, `Report`, `ReportMeeting`, `ScheduledMeeting`
- [x] `adapters/db/database.py` — init de DB, creación de tablas, FTS5 (`search_index`), seed meeting_type
- [x] `adapters/fs/writer.py` — write-temp + rename atómico
- [x] `adapters/fs/paths.py` — resolución de rutas (data_root, archive, import, stats…)
- [x] `adapters/fs/filesystem.py` — implementación real de `FileSystemPort`
- [x] `adapters/fs/agents_md.py` — generación de `AGENTS.md` desde plantilla Jinja2
- [x] `adapters/fs/templates_publisher.py` — publicación de `templates/` en data_root
- [x] `logging_setup.py` — logging con rotación en `TLA_LOG_DIR`

## UI

- [ ] Pantalla de primer arranque (wizard): crear cuenta + confirmar data_root → **delegado a 002-authentication**
- [ ] Banner de recomendación FDE del SO → **delegado a 002-authentication**
- [ ] Arranque normal: ir a lock-screen si hay cuenta, wizard si no → **delegado a 002-authentication**

## Tests

- [x] Test unitario: `InitializeDataRoot` (FS mockeado) — 5 casos
- [x] Test unitario: `PublishSchema` — 2 casos
- [x] Test integración: creación de tablas SQLite en memoria — 4 casos
- [x] Test integración: `writer.py` con FS temporal — 5 casos (PR anterior)

## Notas

La UI de primer arranque requiere el sistema de autenticación. Se implementa en `feature/002-authentication` junto con el lock-screen.
