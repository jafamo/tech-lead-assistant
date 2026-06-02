# Spec: Filesystem — estructura de directorios de miembro

## Port `MemberFileSystemPort` (ABC, en `domain/ports/`)

```python
class MemberFileSystemPort(ABC):
    def initialize_member_dir(self, data_root: Path, slug: str, full_name: str, role: Optional[str]) -> None: ...
    def archive_member_dir(self, data_root: Path, slug: str) -> None: ...
    def reactivate_member_dir(self, data_root: Path, slug: str) -> None: ...
    def member_dir_exists(self, data_root: Path, slug: str) -> bool: ...
```

## Estructura de directorios creada por `initialize_member_dir`

```
{data_root}/{slug}/
  profile/
    profile.md        ← generado desde plantilla Jinja2
  oneToOne/
  seguimiento/
  feedback/
  tecnica/
  retro/
  notes/
  reports/
```

## Plantilla `profile.md.j2` (`src/tla/templates/profile.md.j2`)

```markdown
# {{ full_name }}

**Rol**: {{ role or "—" }}
**Slug**: {{ slug }}
**Incorporación**: {{ start_date or "—" }}

## Notas

_Añade aquí información relevante sobre {{ full_name }}._
```

## Operaciones de archivado / reactivación

- **archive**: `shutil.move` de `{data_root}/{slug}/` → `{data_root}/_archive/{slug}/`
  - Si `_archive/` no existe, crearlo primero
  - Si ya existe `_archive/{slug}/` → raise `AtomicWriteError`
- **reactivate**: `shutil.move` de `{data_root}/_archive/{slug}/` → `{data_root}/{slug}/`
  - Si ya existe `{data_root}/{slug}/` → raise `AtomicWriteError`

## Adapter `LocalMemberFileSystem` (`adapters/fs/member_fs.py`)

Implementa `MemberFileSystemPort` usando `pathlib` + `shutil`. Usa `atomic_write_text` de `fs/writer.py` para el `profile.md`.
