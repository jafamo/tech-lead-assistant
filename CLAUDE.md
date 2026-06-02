# CLAUDE.md — Tech Lead Assistant (TLA)

## Contexto obligatorio

Lee siempre antes de cualquier tarea:

- `ai/context/architecture.md` — stack, estructura, decisiones técnicas.
- `ai/context/business.md` — qué hace la app y por qué.
- `ai/context/coding-standards.md` — convenciones de código.
- `ai/context/glossary.md` — terminología del dominio.

## Reglas por área

- Backend / servicios: `ai/rules/backend.md`
- UI / páginas: `ai/rules/ui.md`
- Seguridad: `ai/rules/security.md`

## Especificaciones (SDD)

Las specs de cada feature están en `ai/specs/NNN-nombre/`:
- `requirements.md` — qué hay que hacer.
- `design.md` — cómo se va a hacer.
- `tasks.md` — tareas concretas con checklist.

Cuando trabajes en una feature, lee la spec correspondiente **completa** antes de escribir código.

## Spec general

La especificación completa de la app está en:
- `docs/specifications/tech_lead_assistant_spec.md`

## Estructura del código fuente (hexagonal)

```
src/tla/
  domain/
    entities/      # modelos de dominio (sin dependencias externas)
    use_cases/     # casos de uso (llaman solo a ports)
    ports/         # interfaces abstractas (ABCs)
    exceptions.py
  adapters/
    db/            # SQLModel — implementa ports de repositorio
    fs/            # scanner, writer atómico, paths
    llm/           # Anthropic, OpenAI, Ollama
    exporters/     # PDF, Markdown, CSV, ICS
    charts/        # Plotly + Kaleido
    ui/            # páginas y componentes NiceGUI
  config.py        # carga .env
  auth.py          # login / lock-screen
  templates/       # Jinja2 internos
```

**Regla de oro**: domain/ no importa nada de adapters/. Las dependencias van siempre hacia dentro.

## Git — Gitflow

| Rama | Origen | Destino | Cuándo |
|---|---|---|---|
| `main` | — | — | Producción. Solo recibe merges de `release/*` y `hotfix/*` |
| `develop` | — | — | Integración. Base de todas las features |
| `feature/NNN-nombre` | `develop` | `develop` | Nueva funcionalidad (NNN = número de spec) |
| `release/<version>` | `develop` | `main` + `develop` | Preparación de release |
| `hotfix/<nombre>` | `main` | `main` + `develop` | Fix urgente en producción |

Commits: Conventional Commits — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.

## Comandos útiles

```bash
# Arrancar (modo dev, primer plano)
./scripts/tla.sh

# Arrancar como servicio systemd (instalar una vez)
./scripts/tla-service.sh install
./scripts/tla-service.sh start
./scripts/tla-service.sh logs     # seguir logs
./scripts/tla-service.sh stop

# Tests
pytest tests/
pytest tests/unit/          # solo unitarios
pytest tests/integration/   # solo integración

# Lint y type check
ruff check src/
mypy src/tla/
```

## Flujo de trabajo con OpenSpec

Usa OpenSpec para cualquier feature o cambio no trivial antes de escribir código.

| Comando | Cuándo usarlo |
|---|---|
| `/opsx:propose "descripción"` | Iniciar un nuevo feature — genera proposal, design y tasks |
| `/opsx:apply` | Implementar lo que está en la spec activa |
| `/opsx:explore` | Explorar el codebase antes de proponer |
| `/opsx:sync` | Sincronizar specs con el estado real del código |
| `/opsx:archive` | Archivar un change completado |

Los changes activos viven en `.openspec/`. Las specs de referencia permanentes van en `ai/specs/NNN-nombre/`.

## Comandos y skills TLA

Skills para operar sobre el data_root:

| Skill / Command | Qué hace |
|---|---|
| `tla-generate-report` | Genera `content.json` desde transcripciones de un miembro |
| `tla-generate-stats` | Genera estadísticas de equipo en `_stats/current/` |
| `/tla:validate-report` | Valida un `content.json` contra el schema |
| `/tla:new-member` | Scaffoldea la estructura de directorios de un nuevo miembro |

Prompts de referencia en `ai/prompts/`.

## Reglas globales

1. Nunca edites ficheros en `data_root` sin usar escritura atómica (write-temp + rename).
2. El índice SQLite es derivable del filesystem. Si dudas, el filesystem gana.
3. Todas las rutas vienen de `.env` vía `config.py`. Nunca hardcodees paths.
4. Los timestamps se almacenan en UTC; la UI los muestra en hora local.
5. Toda operación de UI debe tener feedback visual (spinner, toast, barra de progreso).
6. Cada team_member tiene un color asignado — úsalo como acento en gráficos y UI.
