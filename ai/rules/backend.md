# Reglas: Backend Python

## Configuración
- Todas las rutas, credenciales y flags vienen de `config.py` que carga `.env`.
- Nunca hardcodear rutas. Usar `Config.data_root`, `Config.db_path`, etc.
- Si una variable de `.env` está vacía, usar el default per-OS definido en `config.py`.

## Filesystem
- Todas las escrituras a `data_root` usan `fs/writer.py` (write-temp + rename atómico).
- Nunca usar `open(path, 'w')` directamente sobre `data_root`.
- Las lecturas deben tolerar `FileNotFoundError` y `PermissionError` — loggear y continuar.
- Usar `pathlib.Path` para todo.
- Las rutas en la BD son **relativas a data_root**, nunca absolutas.

## Base de datos
- SQLite es un índice/cache. Si se pierde, se reconstruye con rescan.
- No almacenar contenido de transcripciones ni reports en la BD — solo metadata y hashes.
- Siempre incluir `created_at` y `updated_at` en todos los modelos.
- Transacciones explícitas para operaciones multi-tabla.

## Arquitectura hexagonal — reglas de capas
- **Domain** (`domain/`): sin imports de `adapters/`, `ui/`, `db/`, ni frameworks externos.
- **Ports** (`domain/ports/`): solo ABCs. Sin lógica de negocio ni imports de adapters.
- **Use cases** (`domain/use_cases/`): reciben y devuelven entidades de dominio. Llaman solo a ports.
- **Adapters** (`adapters/`): implementan ports. Pueden usar SQLModel, pathlib, NiceGUI, etc.
- La UI llama a use cases, nunca a repositorios directamente.
- Los errores de negocio se levantan como excepciones custom en `domain/exceptions.py`.

## Servicios / Use cases
- Cada use case opera sobre un dominio (members, meetings, reports, calendar, stats).
- Reciben y devuelven datos tipados (entidades de dominio o Pydantic), nunca dicts crudos.
- Los use cases NO importan nada de `adapters/ui/`. Comunicación unidireccional: UI → use case.

## LLM
- Los proveedores implementan el port `LLMPort` en `domain/ports/llm.py`.
- Las implementaciones concretas viven en `adapters/llm/`.
- El prompt se genera con Jinja2 desde `templates/llm_prompt.j2`.
- La respuesta se valida contra el Pydantic model antes de aceptarla.
- Timeout configurable. Cancelación desde la UI.
- Loggear el prompt enviado y la respuesta recibida en nivel DEBUG (nunca en INFO+).

## Exporters
- Los exporters reciben un `content.json` parseado (Pydantic model) y producen un fichero.
- PDF: Jinja2 → HTML → motor de rendering (WeasyPrint u otro).
- Los charts PNG se generan con Plotly + Kaleido; si Kaleido falla, se omiten sin bloquear.

## Tests unitarios (obligatorio)
- Todo use case tiene su fichero `tests/unit/domain/use_cases/test_<use_case>.py`.
- Los ports se mockean — los tests no tocan DB, filesystem ni red.
- Casos mínimos por use case: caso feliz, error de negocio, entidad no encontrada.
- Las entidades de dominio se testean en `tests/unit/domain/entities/`.
- Nunca escribir un use case sin su test correspondiente — se considera incompleto.
