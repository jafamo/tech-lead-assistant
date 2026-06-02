# 003 — Gestión del Equipo: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Entidad `TeamMember` (slug, full_name, role, color, status, archived_at…)
- [ ] Use case `CreateMember` — valida datos, genera slug, asigna color round-robin
- [ ] Use case `RenameMember` — nuevo slug, mueve carpeta
- [ ] Use case `ArchiveMember` — mueve a `_archive/`, actualiza status
- [ ] Use case `ReactivateMember` — mueve de vuelta, limpia archived_at
- [ ] Use case `UpdateMemberColor` — cambia color
- [ ] Use case `ListMembers` — activos, archivados, con filtros
- [ ] Port `MemberRepository` — interfaz CRUD
- [ ] Port `MemberDirectoryPort` — interfaz para operaciones de FS de miembro
- [ ] Tests unitarios de todos los use cases

## Adapters

- [ ] `adapters/db/member_repo.py` — implementa `MemberRepository`
- [ ] `adapters/fs/member_fs.py` — crea/mueve/archiva estructura de directorios
- [ ] Plantilla Jinja2 `profile.md.j2` → genera `profile/profile.md`
- [ ] Asignación de color automática (round-robin sobre paleta de 12)

## UI

- [ ] `adapters/ui/pages/member_detail.py` — vista de detalle con timeline y color de acento
- [ ] `adapters/ui/pages/member_archive.py` — sección de archivados con "Reactivar"
- [ ] Formulario de creación/edición de miembro (modal)
- [ ] Color picker en formulario de miembro
- [ ] Búsqueda y ordenación en tabla de miembros

## Tests

- [ ] Test unitario: `CreateMember` — slug generado, color asignado, colisión de slug
- [ ] Test unitario: `ArchiveMember` / `ReactivateMember`
- [ ] Test integración: `MemberRepository` contra SQLite en memoria
- [ ] Test integración: creación de estructura de directorios en FS temporal
