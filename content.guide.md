# Guía de `content.json` — explicación campo a campo

Esta guía complementa `content.example.json`. Lee primero el ejemplo para tener una imagen completa, y luego usa esta guía como referencia para cada campo.

> **Regla general**: el schema en `_system/schema/content.schema.json` es la fuente de verdad. Esta guía es el comentario humano.

---

## Estructura general

```
content.json
├── metadata          (información sobre el report en sí)
└── content           (los datos sustantivos del report)
```

---

## `metadata`

Información sobre el report como artefacto: quién, cuándo, cómo se generó.

### `team_member_slug` *(string, requerido)*
Slug de la persona. Debe coincidir con el nombre del directorio donde vive el report.
- Formato: `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$`
- Ejemplo: `"maria-lopez"`

### `period_start` *(string ISO date, requerido)*
Fecha de inicio del periodo cubierto.
- Ejemplo: `"2026-05-01"`

### `period_end` *(string ISO date, requerido)*
Fecha de fin del periodo, inclusiva.
- Ejemplo: `"2026-05-31"`

### `period_label` *(string, opcional)*
Etiqueta legible del periodo. Si no se proporciona, la app deriva una de las fechas.
- Ejemplos: `"2026-05"`, `"2026-Q2"`, `"mayo-2026"`, `"sprint-23"`

### `version` *(integer ≥ 1, requerido)*
Número de versión del report. Debe ser único por `(persona, periodo)`.
- Si regeneras y quieres conservar el anterior: incrementa.
- Si sobrescribes: mantén el mismo número pero asegúrate de que la carpeta tiene el sufijo correcto.

### `generation_mode` *(enum, requerido)*
Cómo se generó el report.
- `"llm"`: la app lo generó llamando a un LLM.
- `"manual"`: el usuario lo rellenó a mano desde el formulario.
- `"imported"`: lo creó una herramienta externa (típicamente, este caso).

### `llm_provider` *(string | null)*
Si `generation_mode = "llm"`: `"anthropic"` | `"openai"` | `"ollama"`. Si no, `null`.

### `llm_model` *(string | null)*
Modelo concreto usado. Ej. `"claude-sonnet-4-7"`, `"gpt-5"`, `"llama3.1:70b"`.

### `created_at` *(string ISO datetime, opcional pero recomendado)*
Timestamp ISO 8601 con zona horaria.
- Ejemplo: `"2026-06-01T10:00:00Z"`

### `source_meetings` *(array de strings, opcional pero recomendado)*
Lista de transcripciones usadas como entrada. Rutas relativas a `data_root`.
- Ejemplo: `["maria-lopez/oneToOne/2026-05-11.transcript.vtt"]`
- **Importante para trazabilidad**: la app usa esto para mostrar "este report cubre estas reuniones".

---

## `content`

El cuerpo sustantivo del report. Esto es lo que el tech lead lee.

### `summary` *(string, requerido)*
Resumen ejecutivo del periodo en 2-3 párrafos. Debe responder: ¿qué pasó este mes con esta persona?

### `key_themes` *(array de objetos)*
Temas que han aparecido repetidamente. Cada uno con:

- **`theme`** *(string, requerido)*: descripción breve. Ej. `"Tech debt en servicio de pagos"`.
- **`frequency`** *(integer ≥ 0)*: número de veces que aparece en las transcripciones del periodo.
- **`evolution`** *(enum)*: `"creciente"` | `"estable"` | `"decreciente"`. Cómo evoluciona vs periodo anterior.
- **`first_mentioned`** *(date | null)*: primera fecha en que se menciona en el histórico conocido. Útil para detectar temas que llevan mucho tiempo sin resolverse.

### `action_items` *(objeto con `open` y `closed`)*

#### `open` *(array de objetos)*
Action items abiertos al final del periodo.
- **`description`** *(string, requerido)*: qué hay que hacer.
- **`owner`** *(enum)*: `"member"` (la persona) o `"tech_lead"` (tú).
- **`since`** *(date)*: fecha en que se abrió.
- **`source_meetings`** *(array de strings)*: reuniones donde se mencionó.

#### `closed` *(array de objetos)*
Action items cerrados durante el periodo.
- **`description`** *(string, requerido)*
- **`owner`** *(enum)*: `"member"` | `"tech_lead"`.
- **`closed_on`** *(date)*: fecha de cierre.

### `growth_signals` *(array de strings)*
Señales positivas: aprendizajes, ownership asumido, iniciativas, mentoring, etc.
- Ejemplo: `"Asumió ownership del servicio de pagos"`

### `risks_and_concerns` *(array de strings)*
Riesgos, frustraciones, blockers, banderas rojas. Cosas a tener en el radar.
- Ejemplo: `"Frustración recurrente con la carga de soporte L2"`

### `sentiment` *(objeto)*
Lectura del estado emocional/motivacional de la persona durante el periodo.

- **`overall`** *(enum)*: `"positivo"` | `"neutral"` | `"preocupado"`.
- **`evolution`** *(array de objetos)*: serie temporal con un punto por reunión.
  - **`date`** *(date)*
  - **`score`** *(number, -1 a 1)*: -1 muy negativo, 0 neutral, 1 muy positivo.

> Esta sección alimenta los gráficos de evolución de sentiment en la app y en el PDF.

### `highlights` *(array de strings)*
Momentos destacados que merecen mencionarse en una performance review.
- Ejemplo: `"Propuso nueva estrategia de testing"`

### `next_1on1_brief` *(string)*
Brief de 2-4 frases preparando la próxima 1:1: qué llevar, qué revisar, qué preguntar.
- **Este es el campo de mayor valor operacional**: es lo que el tech lead lee antes de la siguiente 1:1.

---

## Validación

Antes de guardar `content.json` en su sitio final, valida contra el schema:

```bash
# Ejemplo usando ajv-cli
npx ajv-cli validate -s _system/schema/content.schema.json -d content.json
```

O en Python:

```python
import json
from jsonschema import validate

with open("_system/schema/content.schema.json") as f:
    schema = json.load(f)

with open("content.json") as f:
    data = json.load(f)

validate(instance=data, schema=schema)  # lanza si falla
```

Si la app encuentra un `content.json` malformado durante rescan, abre un popup con la ruta y los errores, y marca el report como inválido.

---

## Tolerancia y compatibilidad

- **Campos adicionales** dentro de `metadata` se aceptan (permite extensiones futuras).
- **Campos adicionales** dentro de `content` NO se aceptan (mantiene consistencia de la UI).
- **Campos faltantes obligatorios** marcan el report como inválido.
- Cuando el schema evolucione, los reports antiguos seguirán siendo legibles si los campos obligatorios no cambian.
