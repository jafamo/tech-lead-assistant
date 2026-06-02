# 010 — Settings y Rescan: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Use case `RunRescan` — re-indexa data_root completo
- [ ] Use case `RegenerateAgentsMd` — regenera `AGENTS.md` preservando secciones de usuario
- [ ] Use case `RegenerateTemplates` — actualiza `templates/` en data_root
- [ ] Use case `RepublishSchema` — copia schema a `_published_schema/`
- [ ] Use case `GetDiagnostics` — estado de conexión a data_root, stats, import, LLM
- [ ] Port `DiagnosticsPort` — interfaz para chequear conectividad
- [ ] Tests unitarios de todos los use cases

## Adapters

- [ ] `adapters/fs/scanner.py` — escanea data_root y sincroniza con BD (miembros, reuniones, reports)
  - [ ] Detecta miembros nuevos
  - [ ] Detecta transcripciones nuevas/modificadas (por file_hash)
  - [ ] Detecta reports `imported` nuevos
  - [ ] Detecta reports en staging dir
  - [ ] Detecta ficheros malformados
  - [ ] Detecta miembros en `_archive/` no marcados como archivados
- [ ] Manejo de red caída: timeout configurable, estado "desconectado" sin crash

## UI

- [ ] `adapters/ui/pages/settings.py` — página Settings
  - [ ] Panel "Configuración efectiva" (valores .env, read-only, badges default/override)
  - [ ] Sección overrides runtime (tema, timeout, locale)
  - [ ] Botón "Cambiar password" (modal, requiere password actual)
  - [ ] Botones de mantenimiento (Rescan, Regenerar AGENTS.md, Regenerar templates, Re-publicar schema)
  - [ ] Panel de diagnóstico (data_root, stats_dir, import_dir, LLM, versión)
  - [ ] Gestión de tipos de reunión (CRUD del catálogo)
  - [ ] Toggle tema light / dark / auto
- [ ] Popup de errores detectados en rescan (ruta + error por fichero)
- [ ] Notificación en banner cuando rescan detecta reports en staging

## Tests

- [ ] Test unitario: `RunRescan` — miembros nuevos, reports importados, ficheros malformados
- [ ] Test unitario: `GetDiagnostics`
- [ ] Test integración: `scanner.py` contra FS temporal
