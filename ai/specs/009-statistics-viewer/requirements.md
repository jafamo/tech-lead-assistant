# 009 — Visualizador de Estadísticas

**Prioridad**: 9
**Rama**: `feature/009-statistics-viewer`
**Depende de**: 001-bootstrap, 007-home-navigation

## Descripción

Página de Estadísticas como **visor de ficheros**. La app no genera estadísticas — las consume. Los ficheros los depositan agentes externos (Claude Code, scripts, otros LLMs).

## Requisitos funcionales

Extraídos de §6.14 de la spec:

- **RF-STAT-1**: Leer `{TLA_STATS_DIR}/current/team_overview.json` y renderizar su contenido. Si no existe → estado vacío con instrucciones de cómo generarlo.
- **RF-STAT-2**: Leer `{TLA_STATS_DIR}/current/per_member/{slug}.json` para stats individuales de cada miembro.
- **RF-STAT-3**: Mostrar imágenes de `{TLA_STATS_DIR}/current/charts/` si existen.
- **RF-STAT-4**: Selector de periodo histórico: leer desde `{TLA_STATS_HISTORY_DIR}/{periodo}/`.
- **RF-STAT-5**: Fichero de stats malformado → popup con ruta y error (tolerancia: muestra lo que puede parsear, omite lo que no).
- **RF-STAT-6**: Botón "Preparar contexto para IA" → genera `{TLA_STATS_DIR}/context_for_ai.md` con reports recientes, action items, etc., para pasar a un agente externo.
- **RF-STAT-7**: Exportar la vista actual como PDF.
- **RF-STAT-8**: Renderizado tolerante — la app renderiza con best-effort y no falla si el schema evoluciona.

## Schema de los ficheros

El schema de `team_overview.json` y `per_member/{slug}.json` está documentado en:
- `ai/prompts/stats-generation.md` (prompt de referencia para agentes externos)

Campos esperados en `team_overview.json`:
- `generated_at`, `period`, `members_count`, `team_sentiment_avg`
- `total_open_action_items`, `most_recurring_themes`, `members_at_risk`, `highlights`

## Casos de uso relacionados

- UC9: Ver estadísticas del equipo generadas por IA.
- UC11: Claude Code deposita los ficheros de stats en `TLA_STATS_DIR`.

## Notas

- La app es read-only sobre `TLA_STATS_DIR` — no escribe salvo el fichero `context_for_ai.md`.
- `members_at_risk` es información sensible — renderizar con discreción.
