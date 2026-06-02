# AGENTS.md — Tech Lead Assistant (TLA)

Este directorio (`data_root`) contiene los datos de **Tech Lead Assistant**. Está diseñado para que tanto la aplicación TLA como herramientas externas (Claude Code, Cursor, scripts ad-hoc) puedan leer y producir contenido de forma consistente.

> ⚠️ Este fichero es mantenido automáticamente por la app cuando arranca. La sección **"User notes"** al final es la única que la app respeta entre regeneraciones.

---

## Estructura de directorios

```
{data_root}/
  AGENTS.md                          # este fichero
  README.md                          # documentación humana
  templates/                         # ejemplos para crear contenido manualmente
    README.md
    content.example.json
    content.guide.md
    profile.example.md
    notes.example.md
    participants.example.json
  {slug-persona}/
    profile/
      profile.md                     # perfil del miembro
    oneToOne/
      YYYY-MM-DD.transcript.{ext}    # transcripciones de 1:1s
      YYYY-MM-DD.notes.md            # notas asociadas (opcional)
    seguimiento/
      ...
    feedback/
      ...
    tecnica/
      ...
    retro/
      ...
    notes/
      YYYY-MM-DD[_titulo].md         # notas sueltas no asociadas a una reunión
    reports/
      {periodo}_v{N}_{modo}/
        content.json                 # OBLIGATORIO — datos estructurados del report
        report.md                    # opcional — render markdown
        report.pdf                   # opcional — render PDF
        charts/                      # gráficas PNG (sentiment, action items, themes)
          sentiment_evolution.png
          action_items_evolution.png
          themes_frequency.png
  _shared/
    meetings/
      YYYY-MM-DD_{slug-reunion}/
        transcript.{ext}
        participants.json
        notes.md
```

> El directorio `_system/` mencionado por la app NO vive aquí — está en local de cada máquina (`~/.local/share/tla/` o `%APPDATA%\TLA\`).

---

## Convenciones

- **Slug de persona**: lowercase, sin tildes, espacios → guiones. Ej: "María López" → `maria-lopez`. En caso de colisión: sufijo numérico (`maria-lopez-2`).
- **Tipos de reunión** (catálogo inicial, extensible desde la app): `oneToOne`, `seguimiento`, `feedback`, `tecnica`, `retro`.
- **Fechas**: ISO `YYYY-MM-DD`.
- **Modos de report**: `llm`, `manual`, `imported`.
- **Carpeta de report**: `{periodo}_v{N}_{modo}/`. Ej. `2026-05_v1_llm`, `2026-Q2_v3_imported`. El número de versión es único por `(persona, periodo)`.
- **Escrituras**: si vas a escribir desde fuera, **write-temp + rename atómico** para evitar half-writes, especialmente sobre red.

---

## Cómo crear un report desde fuera (modo `imported`)

Si quieres generar un report con una herramienta externa (típicamente con un LLM) y que la app TLA lo recoja:

1. Decide el periodo y la versión. Ej: `2026-Q2`, `v1`.
2. Crea la carpeta:
   ```
   {slug-persona}/reports/2026-Q2_v1_imported/
   ```
3. Crea dentro `content.json` siguiendo:
   - El **ejemplo válido** en `templates/content.example.json`.
   - La **guía campo a campo** en `templates/content.guide.md`.
   - El **schema completo** que la app publica en `_system/schema/content.schema.json` (en la máquina con la app).
4. Asegúrate de que el campo `metadata.generation_mode` valga `"imported"`.
5. (Opcional) Crea también `report.md` y `report.pdf` en la misma carpeta. Si no, la app los renderizará al detectar la carpeta.
6. La próxima vez que la app arranque, o cuando se pulse "Rescan", el report aparecerá en el historial de la persona con badge `imported`.

### Si el `content.json` está malformado

La app:
- Marca el report como inválido en la base de datos.
- Abre un **popup** con la ruta del fichero y los errores específicos.
- Sigue mostrando los campos que se hayan podido parsear, con una advertencia visible.

---

## Schema esencial de `content.json` (inline)

```json
{
  "metadata": {
    "team_member_slug": "maria-lopez",
    "period_start": "2026-05-01",
    "period_end": "2026-05-31",
    "period_label": "2026-05",
    "version": 1,
    "generation_mode": "imported",
    "llm_provider": null,
    "llm_model": null,
    "created_at": "2026-06-01T10:00:00Z",
    "source_meetings": [
      "maria-lopez/oneToOne/2026-05-11.transcript.vtt",
      "maria-lopez/oneToOne/2026-05-25.transcript.vtt"
    ]
  },
  "content": {
    "summary": "...",
    "key_themes": [
      {
        "theme": "Tech debt servicio de pagos",
        "frequency": 4,
        "evolution": "creciente",
        "first_mentioned": "2026-03-12"
      }
    ],
    "action_items": {
      "open": [
        {
          "description": "Documentar arquitectura del módulo de billing",
          "owner": "member",
          "since": "2026-04-15",
          "source_meetings": ["maria-lopez/oneToOne/2026-04-15.transcript.vtt"]
        }
      ],
      "closed": [
        {
          "description": "Revisar PR de migración a Postgres",
          "owner": "member",
          "closed_on": "2026-05-20"
        }
      ]
    },
    "growth_signals": ["Asumió ownership del servicio de pagos"],
    "risks_and_concerns": ["Frustración recurrente con la carga de soporte L2"],
    "sentiment": {
      "overall": "neutral",
      "evolution": [
        {"date": "2026-05-04", "score": 0.6},
        {"date": "2026-05-18", "score": 0.4}
      ]
    },
    "highlights": ["Propuso una nueva estrategia de testing en la retro"],
    "next_1on1_brief": "Hacer follow-up sobre el documento de arquitectura pendiente y la carga de soporte."
  }
}
```

---

## Reglas de oro para herramientas externas

1. **NUNCA edites `_system/`** — la app lo gestiona y vive fuera de `data_root` de todas formas.
2. **Edición externa de `.md` y `content.json` es bienvenida**. La app sincroniza vía rescan.
3. **Valida `content.json` antes de guardar**. La app respeta `additionalProperties` parcialmente, pero un JSON inválido te abrirá un popup al usuario.
4. **Escrituras atómicas**: write-temp + rename.
5. **No bloquees ficheros** (la app tampoco lo hace). Si dos procesos/máquinas escriben a la vez, last-write-wins. Coordina humanamente.
6. **Respeta los slugs** existentes. No los inventes — léelos del listado de carpetas.

---

## User notes

<!-- Espacio para notas del usuario. La app respeta esta sección entre regeneraciones de AGENTS.md. -->
