# Design: 003 — Gestión del Equipo

## Capas afectadas

| Capa | Ficheros nuevos |
|---|---|
| Domain entity | `domain/entities/member.py` |
| Domain exceptions | `domain/exceptions.py` (añadir 4 clases) |
| Domain port | `domain/ports/member_repository.py`, `domain/ports/member_fs.py` |
| Domain use cases | `domain/use_cases/create_member.py`, `rename_member.py`, `archive_member.py`, `reactivate_member.py`, `list_members.py`, `get_member.py`, `update_member_color.py` |
| FS adapter | `adapters/fs/member_fs.py` |
| DB adapter | `adapters/db/member_repo.py` |
| UI | `adapters/ui/pages/team.py`, `adapters/ui/pages/team_detail.py` |
| Templates | `src/tla/templates/profile.md.j2` |
| Tests unitarios | `tests/unit/domain/use_cases/test_create_member.py`, etc. |
| Tests integración | `tests/integration/test_member_repository.py` |

## Flujo CreateMember

```
UI modal
  → CreateMember(repo, fs, data_root).execute(full_name, role)
      → slug = slugify(full_name) [+ sufijo si colisión]
      → color = PALETTE[repo.count_active() % 12]
      → member = repo.create(slug, full_name, role, color)
      → fs.initialize_member_dir(data_root, slug, full_name, role)
      → return member
```

## Flujo ArchiveMember

```
UI confirm dialog
  → ArchiveMember(repo, fs, data_root).execute(slug)
      → member = repo.get(slug)  →  MemberNotFoundError si None
      → si member.status == "archived"  →  MemberAlreadyArchivedError
      → fs.archive_member_dir(data_root, slug)   [mueve carpeta]
      → repo.archive(slug)                        [actualiza BD]
      → return member actualizado
```

## Decisiones

- **Slug inmutable**: `RenameMember` no toca el slug. La carpeta en disco no se renombra.
- **`profile.md.j2`** en `src/tla/templates/` (misma carpeta que `AGENTS.md.j2`).
- **Entidad de dominio separada del modelo DB**: `domain/entities/member.py` es un `@dataclass` sin dependencia de SQLModel. El repo hace la conversión.
- **`MemberFileSystemPort`** en domain/ports — los use cases de archivado/reactivación necesitan FS, no solo DB.
- **Atomic write** para `profile.md` usando `atomic_write_text` de `adapters/fs/writer.py` a través del adapter.
