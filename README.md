# Tech Lead Assistant (TLA)

Herramienta personal para tech leads que gestionan equipos pequeños (~6 personas). Centraliza transcripciones de reuniones 1:1, genera reports estructurados y visualiza el seguimiento del equipo a lo largo del tiempo.

---

## Stack

### Core

![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NiceGUI](https://img.shields.io/badge/NiceGUI_2.x-4A9EED?style=for-the-badge&logo=vuedotjs&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-009688?style=for-the-badge&logo=fastapi&logoColor=white)

### IA / LLM

![Anthropic](https://img.shields.io/badge/Anthropic-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=llama&logoColor=white)

### Visualización y exportación

![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![WeasyPrint](https://img.shields.io/badge/WeasyPrint_PDF-E74C3C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)

### Calidad

![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)
![mypy](https://img.shields.io/badge/mypy-2A6DB2?style=for-the-badge&logo=python&logoColor=white)

### Plataformas

![Windows](https://img.shields.io/badge/Windows_10+-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)

---

## Qué hace

- **Ingiere transcripciones** de reuniones 1:1, seguimiento, feedback, técnicas y retros.
- **Genera reports** con resumen, temas recurrentes, action items, sentiment y brief para la próxima reunión — via LLM interno o importando reports preparados externamente con IA.
- **Visualiza el historial** de cada miembro: evolución de sentiment, action items abiertos, temas recurrentes.
- **Compara reports** trimestrales para preparar performance reviews.
- **Muestra estadísticas del equipo** generadas por agentes externos.
- **Gestiona el calendario** interno de reuniones con alertas de pendientes.

---

## Arquitectura

TLA sigue una **arquitectura hexagonal (Ports & Adapters)**. El dominio de negocio no depende de ningún framework, base de datos ni UI:

```
Adapters (NiceGUI · SQLModel · FS · LLM · Exporters)
    ↕ Ports (interfaces abstractas)
Domain (entities · use cases · domain services)
```

Los datos viven como **ficheros planos** en `TLA_DATA_ROOT` (local o red). SQLite es solo un índice derivable — si se pierde, se reconstruye con Rescan. Herramientas externas (Claude Code, scripts, otros agentes) son ciudadanos de primera clase sobre los datos.

---

## Requisitos

- Python 3.11+
- Node.js 20+ (solo para tooling de desarrollo: OpenSpec)
- `pip install -r requirements.txt`

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd tla

# 2. Instalar dependencias Python
pip install -e ".[dev]"

# 3. Configurar entorno
cp .env.example .env
# Edita .env — mínimo obligatorio: TLA_DATA_ROOT

# 4. Arrancar
python -m tla
```

La app estará disponible en `http://127.0.0.1:8080`.

---

## Configuración (`.env`)

| Variable | Descripción | Default |
|---|---|---|
| `TLA_DATA_ROOT` | Directorio de datos (local o red SMB/NFS) | — (obligatorio) |
| `TLA_DB_PATH` | Fichero SQLite de índice — **siempre local** | `~/.local/share/tla/tla.db` |
| `TLA_REPORTS_IMPORT_DIR` | Staging dir para reports externos | `{DATA_ROOT}/_import/` |
| `TLA_STATS_DIR` | Estadísticas generadas por IA | `{DATA_ROOT}/_stats/` |
| `TLA_LLM_PROVIDER` | Proveedor LLM: `anthropic`, `openai`, `ollama`, `none` | `none` |
| `TLA_LLM_MODEL` | Modelo a usar (ej. `claude-sonnet-4-7`) | — |
| `TLA_HOST` / `TLA_PORT` | Servidor NiceGUI | `127.0.0.1:8080` |
| `TLA_THEME` | Tema visual: `auto`, `light`, `dark` | `auto` |
| `TLA_SESSION_TIMEOUT_MIN` | Timeout de sesión por inactividad | `30` |

Ver `.env.example` para la referencia completa con todos los valores posibles.

---

## Flujos de trabajo principales

### Generar un report con LLM interno

1. Inicio → fila del miembro → **Generar report**
2. Selecciona periodo y proveedor LLM
3. La app envía las transcripciones al LLM y guarda el report en `data_root/{slug}/reports/{periodo}_v{N}_llm/`

### Preparar un report externamente con IA

1. Vista del miembro → **Preparar contexto para IA** — la app genera `_import/{slug}/context_for_ai.md` con transcripciones + schema + prompt
2. Abre Claude Code o cualquier herramienta de IA y usa ese contexto para generar `content.json`
3. Deposita el `content.json` en `_import/{slug}/content.json`
4. Vista del miembro → **Importar report** — la app valida, previsualiza y mueve el report

### Usar Claude Code directamente sobre los datos

```bash
# En el directorio data_root, Claude Code puede:
# - Generar reports con el skill tla-generate-report
# - Crear nuevos miembros con /tla:new-member
# - Validar content.json con /tla:validate-report
# - Generar estadísticas del equipo con tla-generate-stats
```

Lee `AGENTS.md` para las convenciones del filesystem de datos.

---

## Estructura del repositorio

```
tla/
├── ai/                        # Fuente de verdad del proyecto (agnóstica de herramienta)
│   ├── context/               # Stack, negocio, convenciones, glosario
│   ├── rules/                 # Reglas por área: backend, ui, security
│   ├── prompts/               # Prompts de referencia para LLMs
│   └── specs/                 # Specs por feature (NNN-nombre/)
│       ├── 001-bootstrap/
│       ├── 002-authentication/
│       ├── 003-team-management/
│       ├── 004-transcription-ingestion/
│       ├── 005-report-generation/
│       ├── 006-report-visualization/
│       ├── 007-home-navigation/
│       ├── 008-calendar-reminders/
│       ├── 009-statistics-viewer/
│       └── 010-settings-rescan/
│
├── docs/
│   ├── specifications/
│   │   └── tech_lead_assistant_spec.md   # Especificación completa
│   └── templates/                        # Plantillas y ejemplos para herramientas externas
│       ├── content.example.json          # Ejemplo válido de content.json
│       ├── profile.example.md            # Ejemplo de profile.md
│       ├── notes.example.md              # Ejemplo de notas de reunión
│       └── participants.example.json     # Ejemplo de participantes multi-miembro
│
├── src/tla/
│   ├── domain/                # Núcleo hexagonal (sin dependencias externas)
│   │   ├── entities/          # TeamMember, Report, Meeting…
│   │   ├── use_cases/         # GenerateReport, ImportReport, ArchiveMember…
│   │   ├── ports/             # Interfaces abstractas (repositorios, LLM…)
│   │   └── exceptions.py
│   ├── adapters/              # Implementaciones de los ports
│   │   ├── db/                # SQLModel
│   │   ├── fs/                # Scanner, writer atómico
│   │   ├── llm/               # Anthropic, OpenAI, Ollama
│   │   ├── exporters/         # PDF, Markdown, CSV, ICS
│   │   ├── charts/            # Plotly + Kaleido
│   │   └── ui/                # Páginas y componentes NiceGUI
│   ├── config.py
│   ├── auth.py
│   └── templates/             # Jinja2 internos
│
├── tests/
│   ├── unit/domain/           # Tests de use cases y entities (ports mockeados)
│   ├── integration/           # Adapters contra SQLite en memoria / FS temporal
│   └── e2e/                   # Flujos completos desde la UI
│
├── .claude/                   # Configuración Claude Code
│   ├── skills/                # tla-generate-report, tla-generate-stats
│   └── commands/tla/          # /tla:validate-report, /tla:new-member
├── .github/
│   └── copilot-instructions.md
│
├── CLAUDE.md                  # Instrucciones para Claude Code
├── AGENTS.md                  # Convenciones del data_root para agentes externos
├── .env.example
├── content.schema.json        # Schema JSON canónico del content.json
└── content.guide.md           # Guía campo a campo del content.json
```

---

## Estructura del data_root

```
{TLA_DATA_ROOT}/
├── AGENTS.md                  # Convenciones para herramientas externas
├── {slug-miembro}/
│   ├── profile/profile.md
│   ├── oneToOne/              # Transcripciones: YYYY-MM-DD.transcript.{ext}
│   ├── seguimiento/
│   ├── feedback/
│   ├── tecnica/
│   ├── retro/
│   ├── notes/
│   └── reports/
│       └── {periodo}_v{N}_{modo}/
│           ├── content.json   # Datos estructurados (schema TLA)
│           ├── report.md
│           ├── report.pdf
│           └── charts/
├── _import/                   # Staging dir para reports externos
├── _stats/current/            # Estadísticas generadas por IA
├── _archive/                  # Miembros archivados
└── _shared/meetings/          # Reuniones multi-participante
```

**Modos de report**: `llm` (generado internamente) · `manual` (importado desde staging) · `imported` (detectado por rescan)

---

## Desarrollo

### Comandos

```bash
pytest tests/                  # todos los tests
pytest tests/unit/             # solo unitarios (sin DB, sin red)
pytest tests/integration/      # adapters contra recursos reales
ruff check src/                # lint
mypy src/tla/                  # type check
```

### Gitflow

| Rama | Cuándo |
|---|---|
| `main` | Producción — solo recibe merges de `release/*` y `hotfix/*` |
| `develop` | Integración — base de todas las features |
| `feature/NNN-nombre` | Nueva funcionalidad (NNN = número de spec en `ai/specs/`) |
| `release/<version>` | Preparación de release |
| `hotfix/<nombre>` | Fix urgente en producción |

Commits: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).

### Flujo de desarrollo con OpenSpec

```bash
/opsx:propose "descripción del feature"   # genera proposal + design + tasks
/opsx:apply                               # implementa la spec activa
/opsx:sync                                # sincroniza specs con el código
/opsx:archive                             # archiva el change completado
```

### Tests unitarios

Todo use case requiere su test en `tests/unit/domain/use_cases/`. Los ports se mockean — ningún test unitario toca DB, filesystem ni red. Cobertura mínima: 90% en `domain/`.

---

## Seguridad

TLA no cifra los datos — los ficheros viven en plano para permitir composabilidad con herramientas externas. La seguridad se delega al **Full Disk Encryption del SO** (BitLocker, LUKS, FileVault). La app lo recuerda en el primer arranque.

El login es un lock-screen de la UI, no un mecanismo de cifrado. Las API keys solo van en `.env` (nunca en la BD ni en logs).

---

## Especificación completa

`docs/specifications/tech_lead_assistant_spec.md`
