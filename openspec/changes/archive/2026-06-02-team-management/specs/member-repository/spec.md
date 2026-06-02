# Spec: DB Adapter — SQLMemberRepository

## `SQLMemberRepository` (`adapters/db/member_repo.py`)

Implementa `MemberRepository` sobre `SQLModel Session` usando el modelo `TeamMember` ya definido en `adapters/db/models.py`.

### Mapeo domain entity ↔ DB model

El use case recibe y devuelve `domain.entities.member.TeamMember` (dataclass). El repo convierte internamente a/desde el modelo SQLModel.

### Método `create`

```python
def create(self, slug, full_name, role, color) -> DomainTeamMember:
    record = DBTeamMember(slug=slug, full_name=full_name, role=role, color=color)
    self._session.add(record)
    self._session.commit()
    self._session.refresh(record)
    return self._to_domain(record)
```

### Método `count_active`

```python
def count_active(self) -> int:
    return self._session.exec(
        select(func.count()).where(DBTeamMember.status == "active")
    ).one()
```

### Métodos `archive` / `reactivate`

Actualizan `status`, `archived_at` y `updated_at` en la misma transacción.

### Conversión `_to_domain`

```python
def _to_domain(self, record: DBTeamMember) -> DomainTeamMember:
    return DomainTeamMember(
        id=record.id,
        slug=record.slug,
        full_name=record.full_name,
        ...
    )
```

## Tests de integración (`tests/integration/test_member_repository.py`)

- `test_create_and_get`
- `test_list_active_empty`
- `test_list_active_returns_only_active`
- `test_archive_and_reactivate`
- `test_count_active`
- `test_update_color`
- `test_rename`
