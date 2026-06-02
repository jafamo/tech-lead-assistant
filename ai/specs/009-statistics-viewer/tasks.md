# 009 — Visualizador de Estadísticas: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Use case `LoadTeamStats` — lee y parsea `team_overview.json`, tolerante a campos desconocidos
- [ ] Use case `LoadMemberStats` — lee `per_member/{slug}.json`
- [ ] Use case `ListStatsHistory` — lista periodos disponibles en `history/`
- [ ] Use case `PrepareStatsAIContext` — genera `context_for_ai.md` con datos de reports actuales
- [ ] Tests unitarios de todos los use cases

## Adapters

- [ ] `adapters/fs/stats_reader.py` — lee JSON de stats con tolerancia a campos extra/ausentes
- [ ] Generación de `context_for_ai.md` desde plantilla Jinja2

## UI

- [ ] `adapters/ui/pages/statistics.py` — página Estadísticas
  - [ ] Sección team overview (sentiment avg, AI open count, members at risk)
  - [ ] Sección most recurring themes
  - [ ] Sección per-member stats (expandible)
  - [ ] Imágenes de `charts/` si existen
  - [ ] Selector de periodo histórico
  - [ ] Estado vacío con instrucciones si no hay ficheros
- [ ] Popup de error si fichero malformado
- [ ] Botón "Preparar contexto para IA"
- [ ] Botón "Exportar como PDF"

## Tests

- [ ] Test unitario: `LoadTeamStats` — fichero válido, campos extra ignorados, fichero ausente
- [ ] Test unitario: `LoadMemberStats`
- [ ] Test unitario: `ListStatsHistory`
- [ ] Test unitario: `PrepareStatsAIContext`
