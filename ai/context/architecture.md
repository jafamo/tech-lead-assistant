# Arquitectura

## Stack

- **Lenguaje**: Python 3.11+
- **UI Framework**: NiceGUI 2.x (internamente FastAPI + Vue.js, corre como servidor local en `localhost`)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Base de datos**: SQLite (siempre local, fichero único)
- **Gráficos**: Plotly (interactivo en UI) + Kaleido (export PNG estático)
- **Templates**: Jinja2
- **PDF**: WeasyPrint (o alternativa: pdfkit, Chromium headless — pendiente de decisión)
- **Validación**: Pydantic + jsonschema
- **Config**: python-dotenv (.env como fuente primaria)

## Principios arquitectónicos

### Filesystem-first
Los datos viven como ficheros planos organizados por persona en `TLA_DATA_ROOT`. La app lee y escribe ficheros pero no reclama propiedad exclusiva. Herramientas externas (Claude Code, scripts) pueden operar sobre los mismos datos.

### La app es un visualizador
La generación de contenido puede ocurrir dentro de la app (modo LLM) o fuera (modo manual/imported). La app trata todos los reports igual independientemente de su procedencia.

### Índice local, datos posiblemente remotos
- SQLite siempre local (`TLA_DB_PATH`).
- `TLA_DATA_ROOT`, `TLA_STATS_DIR`, `TLA_REPORTS_IMPORT_DIR` pueden estar en red (SMB/NFS).
- El índice es derivable: se reconstruye desde el filesystem vía rescan.

### Configuración centralizada
Todo configurable vía `.env`. Todas las rutas, credenciales, flags.

## Estructura de datos (runtime)

```
{TLA_DATA_ROOT}/           # datos canónicos (personas, transcripciones, reports)
{TLA_DB_PATH}              # SQLite índice (siempre local)
{TLA_REPORTS_IMPORT_DIR}/  # staging dir para reports externos
{TLA_STATS_DIR}/           # estadísticas generadas por IA
{TLA_LOG_DIR}/             # logs de la app
```

## Arquitectura hexagonal (Ports & Adapters)

El dominio no depende de ningún framework, base de datos ni UI. Las dependencias siempre apuntan hacia dentro.

```
┌─────────────────────────────────────────────┐
│                  Adapters                   │
│  UI (NiceGUI)  │  DB (SQLModel)  │  FS/LLM  │
├─────────────────────────────────────────────┤
│                   Ports                     │
│  (interfaces: repositorios, servicios LLM)  │
├─────────────────────────────────────────────┤
│                  Domain                     │
│   entities · use cases · domain services    │
└─────────────────────────────────────────────┘
```

### Reglas de dependencia
- **Domain**: sin imports de `adapters/`, `ui/`, `db/`, ni frameworks externos. Solo stdlib y Pydantic.
- **Ports**: ABCs que el dominio define y los adapters implementan.
- **Adapters**: implementan los ports. Pueden importar SQLModel, NiceGUI, pathlib, etc.
- La UI llama a use cases, nunca a repositorios directamente.
- Los use cases solo conocen ports (interfaces), nunca implementaciones concretas.

### Estructura de capas en `src/tla/`

```
domain/
  entities/        → modelos de dominio (TeamMember, Report, Meeting…)
  use_cases/       → casos de uso (GenerateReport, ImportReport, ArchiveMember…)
  ports/           → interfaces abstractas (MemberRepository, LLMPort, ReportWriter…)

adapters/
  db/              → implementaciones SQLModel de los repositorios
  fs/              → scanner, writer atómico, paths
  llm/             → Anthropic, OpenAI, Ollama
  exporters/       → PDF, Markdown, CSV, ICS
  ui/              → páginas y componentes NiceGUI

config.py          → carga .env, resuelve defaults
auth.py            → login, bcrypt, sesión
```

## Flujo de datos

```
UI (adapter)
    ↓ llama a
Use Case (domain)
    ↓ llama a port (interfaz)
        ↓ implementado por adapter (DB / FS / LLM)
```

## Escrituras atómicas

Todas las escrituras a `data_root` (que puede ser red) usan el patrón write-temp + rename:

```python
import tempfile, os

def atomic_write(path, content):
    dir = os.path.dirname(path)
    with tempfile.NamedTemporaryFile(mode='w', dir=dir, delete=False, suffix='.tmp') as f:
        f.write(content)
        tmp = f.name
    os.replace(tmp, path)  # atómico en POSIX, best-effort en Windows
```

## Decisiones técnicas documentadas

Ver `docs/decisions/` para ADRs formales. Resumen:

- **SQLite siempre local**: evitar problemas de file locking sobre SMB/NFS.
- **Ficheros en plano**: composability con herramientas externas prima sobre seguridad de datos.
- **Tres modos de report**: `llm` (interno), `manual` (staging dir), `imported` (detección automática).
- **Estadísticas como visor**: la app no genera stats, las visualiza desde ficheros de IA.
- **Calendario interno + .ics**: sin API directa con Google/Outlook en v1.
