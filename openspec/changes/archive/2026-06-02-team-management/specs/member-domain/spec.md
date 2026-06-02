# Spec: Domain — entidad, port y use cases de TeamMember

## Entidad `TeamMember` (domain)

```python
@dataclass
class TeamMember:
    id: int
    slug: str
    full_name: str
    role: Optional[str]
    color: str          # hex
    status: str         # "active" | "archived"
    start_date: Optional[date]
    archived_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

## Port `MemberRepository` (ABC)

```python
class MemberRepository(ABC):
    def create(self, slug: str, full_name: str, role: Optional[str], color: str) -> TeamMember: ...
    def get(self, slug: str) -> Optional[TeamMember]: ...
    def list_active(self) -> list[TeamMember]: ...
    def list_archived(self) -> list[TeamMember]: ...
    def count_active(self) -> int: ...
    def rename(self, slug: str, new_full_name: str, new_role: Optional[str]) -> TeamMember: ...
    def archive(self, slug: str) -> TeamMember: ...
    def reactivate(self, slug: str) -> TeamMember: ...
    def update_color(self, slug: str, color: str) -> TeamMember: ...
```

## Use cases

### `CreateMember`
- Recibe: `full_name`, `role` (opcional)
- Genera slug: slugify(full_name), colisión → añade sufijo `-2`, `-3`, …
- Asigna color: `PALETTE[repo.count_active() % 12]`
- Llama a `repo.create(...)` → `TeamMember`
- Llama a `fs.initialize_member_dir(data_root, slug, full_name, role)`
- Devuelve `TeamMember`
- Excepción: `MemberAlreadyExistsError` (slug colisión no resoluble — no aplica en práctica)

### `RenameMember`
- Recibe: `slug`, `new_full_name`, `new_role`
- Slug NO cambia
- Llama a `repo.rename(slug, new_full_name, new_role)`
- Devuelve `TeamMember` actualizado
- Excepción: `MemberNotFoundError`

### `ArchiveMember`
- Recibe: `slug`
- Llama a `fs.archive_member_dir(data_root, slug)` — mueve `{data_root}/{slug}/` → `{data_root}/_archive/{slug}/`
- Llama a `repo.archive(slug)`
- Devuelve `TeamMember` actualizado
- Excepción: `MemberNotFoundError`, `MemberAlreadyArchivedError`

### `ReactivateMember`
- Recibe: `slug`
- Llama a `fs.reactivate_member_dir(data_root, slug)` — mueve de `_archive/` a raíz
- Llama a `repo.reactivate(slug)`
- Devuelve `TeamMember` actualizado
- Excepción: `MemberNotFoundError`, `MemberNotArchivedError`

### `ListMembers`
- Recibe: `include_archived: bool = False`
- Devuelve `list[TeamMember]`

### `GetMember`
- Recibe: `slug`
- Devuelve `TeamMember`
- Excepción: `MemberNotFoundError`

### `UpdateMemberColor`
- Recibe: `slug`, `color` (hex válido `#RRGGBB`)
- Llama a `repo.update_color(slug, color)`
- Devuelve `TeamMember` actualizado
- Excepción: `MemberNotFoundError`, `InvalidColorError`

## Excepciones (en `domain/exceptions.py`)

```python
class MemberNotFoundError(TLAError): ...
class MemberAlreadyArchivedError(TLAError): ...
class MemberNotArchivedError(TLAError): ...
class InvalidColorError(TLAError): ...
```

## Paleta

```python
# domain/entities/member.py
MEMBER_COLOR_PALETTE = [
    "#4A90D9", "#E67E22", "#27AE60", "#8E44AD", "#E74C3C",
    "#1ABC9C", "#F39C12", "#2980B9", "#D35400", "#16A085",
    "#C0392B", "#7F8C8D",
]
```
