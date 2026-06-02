# 010 — Settings y Rescan

**Prioridad**: 10
**Rama**: `feature/010-settings-rescan`
**Depende de**: 001-bootstrap, 002-authentication

## Descripción

Página de configuración, mantenimiento del índice SQLite mediante rescan del filesystem, y diagnóstico del estado de la app.

## Requisitos funcionales

### Página Settings (§6.15)
- **RF-SET-1**: Mostrar valores efectivos de `.env` (read-only) con badge indicando si es el default o está sobreescrito.
- **RF-SET-2**: Override runtime de settings no sensibles (tema, timeout de sesión, locale) — sin tocar el `.env`.
- **RF-SET-3**: Cambio de password (requiere password actual).
- **RF-SET-4**: Botones de mantenimiento:
  - **Rescan**: re-indexa `data_root` desde cero.
  - **Regenerar AGENTS.md**: regenera el `AGENTS.md` del `data_root` preservando secciones "User notes".
  - **Regenerar templates**: actualiza la carpeta `templates/` del `data_root`.
  - **Re-publicar schema**: copia `content.schema.json` a `_published_schema/`.
- **RF-SET-5**: Panel de diagnóstico:
  - Estado de conexión a `TLA_DATA_ROOT`, `TLA_STATS_DIR`, `TLA_REPORTS_IMPORT_DIR`.
  - Estado del LLM configurado (proveedor, modelo, conectividad).
  - Versión de la app y del schema.
- **RF-SET-6**: Gestión de tipos de reunión: añadir nuevos tipos, editar `display_name` e icono.
- **RF-SET-7**: Toggle de tema visual (light / dark / auto).

### Sincronización (rescan) (§6.16)
- **RF-SYNC-1**: Rescan completo al arrancar (configurable con `TLA_RESCAN_ON_STARTUP`).
- **RF-SYNC-2**: Botón "Rescan" manual en Settings.
- **RF-SYNC-3**: Red caída → estado "desconectado", deshabilitar escrituras.
- **RF-SYNC-4**: Fichero malformado detectado → popup con ruta y errores.
- **RF-SYNC-5**: Detectar reports nuevos en staging dir → notificar en banner.
- **RF-SYNC-6**: Detectar miembros archivados/reactivados desde fuera de la app.

### Rescan — qué detecta
- Miembros nuevos (carpetas en `data_root` no registradas).
- Transcripciones nuevas o modificadas (por `file_hash`).
- Reports nuevos en `reports/` (modo `imported`).
- Reports en staging dir pendientes de importar.
- Ficheros malformados (`content.json` inválido).
- Miembros en `_archive/` no marcados como archivados en BD.

## Requisitos no funcionales

- Rescan < 5 s en local, < 30 s en red (≤ 100 ficheros).
- API keys nunca aparecen en la UI ni en logs.
