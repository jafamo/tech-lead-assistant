# 001 — Bootstrap: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Entidad `Config` o dataclass con todos los paths resueltos
- [ ] Use case `InitializeDataRoot` — crea la estructura de directorios si no existe
- [ ] Use case `PublishSchema` — copia `content.schema.json` a `_published_schema/`
- [ ] Port `FileSystemPort` — interfaz para operaciones de FS (mkdir, exists, copy atómica)
- [ ] Tests unitarios de `InitializeDataRoot` (FS mockeado)

## Adapters

- [ ] `config.py` — carga `.env` con python-dotenv, resuelve defaults por SO, expone `Settings`
- [ ] `adapters/db/models.py` — modelos SQLModel: `User`, `TeamMember`, `MeetingType`, `Meeting`, `MeetingParticipant`, `Report`, `ReportMeeting`, `ScheduledMeeting`
- [ ] `adapters/db/` — init de DB, creación de tablas, FTS5 (`search_index`)
- [ ] Seed de `meeting_type` con tipos por defecto (oneToOne, seguimiento, feedback, tecnica, retro)
- [ ] `adapters/fs/writer.py` — write-temp + rename atómico
- [ ] `adapters/fs/paths.py` — resolución de rutas (data_root, archive, import, stats…)
- [ ] `adapters/fs/agents_md.py` — generación de `AGENTS.md` desde plantilla Jinja2
- [ ] `adapters/fs/templates_publisher.py` — publicación de `templates/` en data_root
- [ ] Logging con rotación en `TLA_LOG_DIR`

## UI

- [ ] Pantalla de primer arranque (wizard): crear cuenta + confirmar data_root
- [ ] Banner de recomendación FDE del SO
- [ ] Arranque normal: ir a lock-screen si hay cuenta, wizard si no

## Tests

- [ ] Test unitario: `InitializeDataRoot` (FS mockeado)
- [ ] Test unitario: `PublishSchema`
- [ ] Test integración: creación de tablas SQLite en memoria
- [ ] Test integración: `writer.py` con FS temporal
