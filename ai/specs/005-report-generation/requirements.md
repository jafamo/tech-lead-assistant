# 005 — Generación de Reports

**Prioridad**: 5 (propuesta de valor principal de la app)
**Rama**: `feature/005-report-generation`
**Depende de**: 001-bootstrap, 003-team-management, 004-transcription-ingestion

## Descripción

Generación de reports estructurados en tres modos: LLM interno, importación desde staging dir (manual), y detección automática en rescan (imported). El report se almacena como `content.json` validado contra schema TLA.

## Modos de report

### Modo `llm` — generación interna
- **RF-REP-LLM-1**: Desde la vista del miembro → "Generar report" → modal para elegir rango de fechas y proveedor LLM.
- **RF-REP-LLM-2**: La app recopila transcripciones del rango, construye el prompt (Jinja2 desde `llm_prompt.j2`), envía al LLM (Anthropic / OpenAI / Ollama), recibe `content.json`.
- **RF-REP-LLM-3**: Validación contra schema → si inválido, popup con errores. Si válido: guarda, genera exports y charts.
- Proveedores: `anthropic`, `openai`, `ollama`. Configurado en `.env`. Modal de confirmación antes de enviar a cloud.

### Modo `manual` — import desde staging dir
- **RF-REP-STAGE-1**: El usuario prepara `content.json` fuera de la app (con Claude Code, ChatGPT, scripts…) y lo deposita en `{TLA_REPORTS_IMPORT_DIR}/{slug}/content.json`.
- **RF-REP-STAGE-2**: Desde la vista del miembro → "Importar report desde staging".
- **RF-REP-STAGE-3**: Preview del contenido + validación. Usuario confirma periodo y versión.
- **RF-REP-STAGE-4**: La app **mueve** (no copia, atómico) a `{TLA_DATA_ROOT}/{slug}/reports/{periodo}_v{N}_manual/content.json`.
- **RF-REP-STAGE-5**: Genera exports (`report.md`, `report.pdf`) y charts PNG.
- **RF-REP-STAGE-6**: Botón "Preparar contexto para IA" → genera `{TLA_REPORTS_IMPORT_DIR}/{slug}/context_for_ai.md` con transcripciones + schema + prompt sugerido.

### Modo `imported` — detección automática
- **RF-REP-IMP-1**: En rescan, detecta carpetas `*_imported/` en `{TLA_DATA_ROOT}/{slug}/reports/` con `content.json` nuevo.
- **RF-REP-IMP-2**: Valida, indexa, genera exports y charts si faltan.

### Comunes a todos los modos
- **RF-REP-COM-1**: El report nace como `draft`. Finalización explícita por el usuario.
- **RF-REP-COM-2**: JSON inválido → popup con ruta y errores, report en estado `schema_invalid`.
- **RF-REP-COM-3**: Todos los reports registran `created_at`, `updated_at`, `generation_mode`, `llm_provider`, `llm_model`.

## Versionado
- **RF-VER-1**: Cada generación crea carpeta `{periodo}_v{N+1}_{modo}/`. No sobreescribe versiones anteriores.
- **RF-VER-2**: Opción "Sobrescribir": reemplaza `content.json` de la última versión, regenera exports y charts.
- **RF-VER-3**: Listado de versiones del filesystem con fechas.

## Gráficos de cada report
- **RF-CHART-1**: PNGs en `charts/`: `sentiment_evolution.png`, `action_items_evolution.png`, `themes_frequency.png`.
- **RF-CHART-2**: Plotly + Kaleido para PNGs. Plotly interactivo en UI.
- **RF-CHART-3**: Si Kaleido falla → warning, omitir PNGs, UI sigue con Plotly interactivo.
- **RF-CHART-4**: Sin datos suficientes → omitir ese gráfico.
- **RF-CHART-5**: Usa el color del miembro como color principal.

## Schema TLA (`content.json`)

Ver `content.schema.json` en la raíz del proyecto. Campos clave:
- `metadata`: `team_member_slug`, `period_start`, `period_end`, `generation_mode`, `version`.
- `content`: `summary`, `key_themes`, `action_items.open`, `action_items.closed`, `growth_signals`, `risks_and_concerns`, `sentiment.overall`, `sentiment.evolution`, `highlights`, `next_1on1_brief`, `source_meetings`.

## Casos de uso relacionados

- UC1: Generar report con LLM.
- UC2: Preparar externamente → importar.
- UC11: Claude Code genera `content.json` directamente.
