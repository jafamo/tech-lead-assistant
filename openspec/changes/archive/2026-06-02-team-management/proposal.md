# Proposal: 003 — Gestión del Equipo

## Objetivo

CRUD completo de miembros del equipo: crear, renombrar, archivar, reactivar y listar, con estructura de directorios automática en `TLA_DATA_ROOT` y asignación de color por paleta round-robin.

## Contexto

Bloque central del dominio — todos los reports, reuniones y estadísticas referencian un `TeamMember`. Sin esta feature no se puede construir nada más. Depende de 001 (filesystem, modelos DB) y 002 (autenticación).

## Alcance

### Incluido

- **Domain**: entidad `TeamMember`, port `MemberRepository`, use cases `CreateMember`, `RenameMember`, `ArchiveMember`, `ReactivateMember`, `ListMembers`, `GetMember`
- **Filesystem**: use case `InitializeMemberDir` — crea `{data_root}/{slug}/` con subdirectorios y `profile/profile.md` desde plantilla Jinja2
- **DB adapter**: `SQLMemberRepository` implementa `MemberRepository`
- **UI**: página `/team` (listado con búsqueda y filtros), `/team/{slug}` (detalle stub), modal de creación, modal de renombrado, confirmación de archivado, sección "archivados" colapsable
- **Color**: paleta de 12 colores round-robin, editable desde detalle del miembro
- **Tests**: unitarios para todos los use cases, integración para `SQLMemberRepository`

### Excluido

- Vista de detalle completa (timeline de reuniones) → feature 005
- Cambio de slug manual por el usuario → riesgo de rotura de historial, out of scope v1

## Decisiones de diseño

1. **Slug inmutable tras creación** — el nombre se puede cambiar, el slug no. Evita romper rutas de filesystem e historial.
2. **Archivado = mover carpeta**, no borrar. Reversible. La ruta en BD es relativa a `data_root`.
3. **`profile.md` desde Jinja2** — template en `src/tla/templates/profile.md.j2`, contexto: `{full_name, role, slug, created_at}`.
4. **Color round-robin** — al crear, se cuenta cuántos miembros activos hay y se toma `PALETTE[count % 12]`.
5. **Port `MemberRepository`** en `domain/ports/` — domain solo lo conoce como ABC.

## Paleta

```python
MEMBER_COLOR_PALETTE = [
    "#4A90D9", "#E67E22", "#27AE60", "#8E44AD", "#E74C3C",
    "#1ABC9C", "#F39C12", "#2980B9", "#D35400", "#16A085",
    "#C0392B", "#7F8C8D",
]
```
