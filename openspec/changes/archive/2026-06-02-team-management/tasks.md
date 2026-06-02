## 1. Domain — Entidad y constantes

- [x] 1.1 Crear `domain/entities/member.py` — dataclass `TeamMember` + `MEMBER_COLOR_PALETTE`
- [x] 1.2 Añadir excepciones a `domain/exceptions.py`: `MemberNotFoundError`, `MemberAlreadyArchivedError`, `MemberNotArchivedError`, `InvalidColorError`

## 2. Domain — Ports

- [x] 2.1 Crear `domain/ports/member_repository.py` — ABC `MemberRepository`
- [x] 2.2 Crear `domain/ports/member_fs.py` — ABC `MemberFileSystemPort`

## 3. Domain — Use cases

- [x] 3.1 `use_cases/create_member.py` — `CreateMember`: slug, color round-robin, crea en repo + FS
- [x] 3.2 `use_cases/rename_member.py` — `RenameMember`: actualiza nombre/rol, slug inmutable
- [x] 3.3 `use_cases/archive_member.py` — `ArchiveMember`: mueve FS + actualiza BD
- [x] 3.4 `use_cases/reactivate_member.py` — `ReactivateMember`: mueve FS + actualiza BD
- [x] 3.5 `use_cases/list_members.py` — `ListMembers`: active o todos
- [x] 3.6 `use_cases/get_member.py` — `GetMember`: por slug
- [x] 3.7 `use_cases/update_member_color.py` — `UpdateMemberColor`: valida hex, persiste

## 4. Domain — Tests unitarios

- [x] 4.1 `tests/unit/domain/use_cases/test_create_member.py` — éxito, colisión de slug, color round-robin
- [x] 4.2 `tests/unit/domain/use_cases/test_rename_member.py` — éxito, not found
- [x] 4.3 `tests/unit/domain/use_cases/test_archive_member.py` — éxito, not found, ya archivado
- [x] 4.4 `tests/unit/domain/use_cases/test_reactivate_member.py` — éxito, not found, no archivado
- [x] 4.5 `tests/unit/domain/use_cases/test_list_members.py` — activos, todos
- [x] 4.6 `tests/unit/domain/use_cases/test_update_member_color.py` — éxito, color inválido, not found

## 5. FS Adapter

- [x] 5.1 Crear `adapters/fs/member_fs.py` — `LocalMemberFileSystem` implementa `MemberFileSystemPort`
- [x] 5.2 Crear plantilla `src/tla/templates/profile.md.j2`

## 6. DB Adapter

- [x] 6.1 Crear `adapters/db/member_repo.py` — `SQLMemberRepository` implementa `MemberRepository`
- [x] 6.2 `tests/integration/test_member_repository.py` — 7 tests contra SQLite en memoria

## 7. UI — Página `/team`

- [x] 7.1 Crear `adapters/ui/pages/team.py` — listado de miembros activos con dot de color y búsqueda
- [x] 7.2 Modal "Añadir miembro" — campos nombre + rol, llama `CreateMember`
- [x] 7.3 Modal "Renombrar" — campos pre-rellenos, llama `RenameMember`
- [x] 7.4 Confirmación "Archivar" — dialog, llama `ArchiveMember`
- [x] 7.5 Color picker — llama `UpdateMemberColor`
- [x] 7.6 Sección "Archivados" colapsable — tabla con botón "Reactivar"

## 8. UI — Página `/team/{slug}`

- [x] 8.1 Crear `adapters/ui/pages/team_detail.py` — stub con nombre, rol y color del miembro

## 9. Routing y navegación

- [x] 9.1 Registrar páginas en `app.py`
- [x] 9.2 Añadir enlace "Ver equipo →" en el index `/`
