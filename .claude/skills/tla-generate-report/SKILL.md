---
name: tla-generate-report
description: Genera un report estructurado (content.json) para un miembro del equipo a partir de sus transcripciones en data_root. Sigue el schema TLA y lo deposita listo para que la app lo detecte via rescan (modo imported).
---

Genera un `content.json` válido para un miembro del equipo a partir de sus transcripciones.

## Pasos

1. **Obtener parámetros** — si no se han proporcionado, pregunta:
   - `slug` del miembro (ej. `maria-lopez`). Léelo del listado de carpetas en `data_root/`.
   - `periodo` (ej. `2026-05`, `2026-Q2`).
   - `data_root` — lee de `.env` o pregunta al usuario.

2. **Leer el perfil del miembro**
   ```
   {data_root}/{slug}/profile/profile.md
   ```

3. **Listar y leer transcripciones del periodo**
   - Busca en `{data_root}/{slug}/oneToOne/`, `seguimiento/`, `feedback/`, `tecnica/`, `retro/`
   - Filtra por fechas dentro del periodo
   - Lee el contenido de cada transcripción

4. **Leer reports anteriores** para contexto histórico
   - `{data_root}/{slug}/reports/` — lee los `content.json` de los últimos 2 reports
   - Extrae: action_items abiertos, key_themes recurrentes, evolución de sentiment

5. **Leer el prompt de referencia**
   - `ai/prompts/report-generation.md`

6. **Generar el `content.json`**
   - Sigue estrictamente el schema en `content.schema.json` (raíz del proyecto)
   - Campo `metadata.generation_mode` = `"imported"`
   - Campo `metadata.team_member_slug` = slug del miembro
   - Incluye todos los `source_meetings` con rutas relativas a `data_root`
   - Lleva los action_items abiertos anteriores al nuevo report como `open` salvo que las transcripciones indiquen que se han cerrado

7. **Determinar versión**
   - Cuenta las carpetas existentes en `{data_root}/{slug}/reports/` con el mismo periodo
   - Versión = N + 1

8. **Escribir atómicamente**
   - Ruta destino: `{data_root}/{slug}/reports/{periodo}_v{N}_imported/content.json`
   - Usa write-temp + rename (crea fichero `.tmp`, luego renombra)
   - También genera `report.md` con un resumen legible en la misma carpeta

9. **Confirmar al usuario**
   - Muestra la ruta donde se ha guardado
   - Indica que la próxima vez que la app haga rescan, el report aparecerá con badge `imported`

## Restricciones

- NUNCA escribas directamente con `open(path, 'w')` — siempre write-temp + rename
- Las rutas en `source_meetings` son **relativas a data_root**, no absolutas
- Si faltan transcripciones para el periodo, avisa al usuario antes de continuar
- Valida el JSON generado contra el schema antes de guardarlo
- Si el `content.json` ya existe en esa carpeta, pregunta antes de sobrescribir
