# Convenciones de código

## Python

- Python 3.11+ con type hints en todas las funciones públicas.
- Formatter: `ruff format`. Linter: `ruff check`. Type checker: `mypy`.
- Docstrings en Google style para funciones y clases públicas.
- Imports ordenados: stdlib → third-party → local (ruff gestiona esto).
- Usar `pathlib.Path` para todas las operaciones con rutas, nunca `os.path`.
- Logs con `logging` estándar, nunca `print()`.
- Excepciones custom en `src/tla/exceptions.py`. Nunca capturar `Exception` genérico salvo en top-level handlers.

## NiceGUI

- Cada página en un fichero separado en `src/tla/ui/pages/`.
- Componentes reutilizables en `src/tla/ui/components/`.
- Separar lógica de negocio (services/) de UI (ui/). Las páginas llaman a servicios, no implementan lógica.
- Usar decoradores `@ui.page` para rutas.
- Feedback visual obligatorio: spinner en operaciones >200ms, toast tras acciones exitosas, popup en errores.

## SQLModel

- Modelos en `src/tla/db/models.py`.
- Siempre incluir `created_at` y `updated_at` en todos los modelos.
- Queries en los servicios, no en las páginas de UI.
- Transacciones explícitas para operaciones multi-tabla.

## Filesystem

- Escrituras atómicas siempre (write-temp + rename).
- Todas las rutas resueltas desde `config.py` (nunca hardcodear).
- Hash de fichero (SHA-256) para detectar cambios en rescan.
- Tolerancia a errores: si un fichero no se puede leer, loggear y continuar.

## Tests

### Unitarios
- Pytest. Un fichero de test por módulo: `tests/unit/domain/test_<módulo>.py`.
- Testean **domain** (use cases, entities, domain services) en aislamiento total.
- Los ports se mockean con `unittest.mock` o `pytest-mock`. Nunca se toca DB, filesystem ni red.
- Nomenclatura: `test_<acción>_<condición>_<resultado_esperado>` (ej. `test_archive_member_active_moves_to_archive`).
- Cobertura mínima target: **90% en `domain/`**.
- Cada use case tiene al menos: caso feliz, caso de error de negocio, caso de entidad no encontrada.

### Integración
- `tests/integration/` — prueban adapters contra recursos reales (SQLite en memoria, filesystem temporal).
- `sample_data_root/` como fixture de filesystem.
- Cobertura mínima target: 70% en `adapters/`.

### E2E / UI
- `tests/e2e/` — flujos completos desde la UI. Cobertura mínima target: 60% en `adapters/ui/`.

### Reglas generales
- Sin `print()` en tests. Usar `capfd` de pytest si hay que capturar output.
- Fixtures compartidas en `tests/conftest.py`.
- Los tests no dependen del orden de ejecución.
- Un test que pasa sin assertions es un bug — usar `pytest-assert` o `assert` explícito siempre.

## Git — Gitflow

Ramas permanentes:
- `main` — producción. Solo recibe merges desde `release/*` y `hotfix/*`.
- `develop` — integración. Base de todas las features.

Ramas de soporte (vida corta):
- `feature/<nombre>` — nueva funcionalidad. Sale de `develop`, merge a `develop`.
- `release/<version>` — preparación de release. Sale de `develop`, merge a `main` y `develop`.
- `hotfix/<nombre>` — fix urgente en producción. Sale de `main`, merge a `main` y `develop`.

Convenciones:
- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.
- Nombre de feature branch referencia la spec: `feature/NNN-nombre` (ej. `feature/001-authentication`).
- PRs siempre hacia `develop` (salvo hotfix/release). Descripción referencia la spec en `ai/specs/NNN-`.
