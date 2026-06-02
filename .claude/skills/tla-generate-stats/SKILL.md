---
name: tla-generate-stats
description: Genera estadísticas del equipo (team_overview.json y per_member/{slug}.json) a partir de los reports existentes en data_root y las deposita en _stats/current/ para que la app TLA las visualice.
---

Genera las estadísticas del equipo leyendo todos los reports del `data_root` y las deposita en `TLA_STATS_DIR/current/`.

## Pasos

1. **Obtener rutas** — lee de `.env`:
   - `TLA_DATA_ROOT` — directorio raíz de datos
   - `TLA_STATS_DIR` — directorio de estadísticas (default: `{TLA_DATA_ROOT}/_stats/`)

2. **Leer el prompt de referencia**
   - `ai/prompts/stats-generation.md`

3. **Descubrir miembros activos**
   - Lista carpetas en `{data_root}/` excluyendo `_archive/`, `_stats/`, `_import/`, `_shared/`, `_published_schema/`
   - Para cada carpeta, verifica que tiene subcarpetas de reunión (`oneToOne/`, etc.)

4. **Por cada miembro, leer sus reports**
   - Lista `{data_root}/{slug}/reports/*/content.json`
   - Ordena por fecha descendente, toma los últimos 6 (o todos si hay menos)
   - Extrae: sentiment evolution, action_items (open/closed), key_themes, highlights, risks

5. **Generar `per_member/{slug}.json`** por cada miembro:
   ```json
   {
     "slug": "...",
     "full_name": "...",
     "periods_analyzed": [...],
     "sentiment_trend": [...],
     "open_action_items": [...],
     "recurring_themes": [...],
     "risks": [...],
     "generated_at": "ISO8601 UTC"
   }
   ```

6. **Generar `team_overview.json`** con agregados del equipo:
   ```json
   {
     "generated_at": "ISO8601 UTC",
     "period": "...",
     "members_count": N,
     "team_sentiment_avg": 0.0,
     "total_open_action_items": N,
     "most_recurring_themes": [...],
     "members_at_risk": [...],
     "highlights": [...]
   }
   ```

7. **Archivar versión anterior** (si existe)
   - Mueve `{TLA_STATS_DIR}/current/` → `{TLA_STATS_DIR}/history/{periodo}/`
   - El periodo es el mes/trimestre más reciente de los reports analizados

8. **Escribir atómicamente** en `{TLA_STATS_DIR}/current/`:
   - `team_overview.json`
   - `team_overview.md` (versión legible en markdown)
   - `per_member/{slug}.json` por cada miembro

9. **Confirmar al usuario**
   - Lista de ficheros generados con sus rutas
   - Indica que la app mostrará las stats al navegar a la página Estadísticas

## Restricciones

- Escrituras siempre write-temp + rename
- Si un `content.json` está malformado, loggea el error y continua con el resto
- No modifica ni elimina reports existentes — es read-only sobre `reports/`
- Si `TLA_STATS_DIR` no existe, lo crea con los subdirectorios necesarios
