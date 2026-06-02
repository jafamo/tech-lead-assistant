# Spec: DB Adapter — SQLMeetingRepository

## `SQLMeetingRepository` (`adapters/db/meeting_repo.py`)

Implementa `MeetingRepository` sobre `SQLModel Session` usando los modelos `Meeting`, `MeetingParticipant`, `MeetingType`, `TeamMember` ya definidos en `adapters/db/models.py`.

### Mapeo domain ↔ DB

El use case recibe/devuelve `domain.entities.meeting.Meeting` (dataclass). El repo resuelve los IDs a slugs para devolver la entidad de dominio.

### `hash_exists`

```python
def hash_exists(self, file_hash: str) -> bool:
    return self._session.exec(
        select(DBMeeting).where(DBMeeting.file_hash == file_hash)
    ).first() is not None
```

### `index_fts`

```python
def index_fts(self, meeting_id: int, content: str, member_slug: str, doc_type: str) -> None:
    # Truncar a 100 KB
    truncated = content[:100_000]
    self._session.exec(text(
        "INSERT INTO search_index(file_path, content, member_slug, doc_type) VALUES (:p, :c, :m, :d)"
    ), {"p": str(meeting_id), "c": truncated, "m": member_slug, "d": doc_type})
    self._session.commit()
```

### `search_fts`

```python
def search_fts(self, query: str, member_slug: Optional[str] = None) -> list[Meeting]:
    base = "SELECT file_path FROM search_index WHERE search_index MATCH :q"
    params: dict = {"q": query}
    if member_slug:
        base += " AND member_slug = :m"
        params["m"] = member_slug
    rows = self._session.exec(text(base), params).fetchall()
    ids = [int(r[0]) for r in rows if r[0].isdigit()]
    meetings = [self._session.get(DBMeeting, mid) for mid in ids]
    return [self._to_domain(m) for m in meetings if m]
```

### `delete` (con FTS)

```python
def delete(self, meeting_id: int) -> None:
    self._session.exec(text("DELETE FROM search_index WHERE file_path = :p"), {"p": str(meeting_id)})
    record = self._session.get(DBMeeting, meeting_id)
    if record:
        self._session.delete(record)
    self._session.commit()
```

## Tests de integración (`tests/integration/test_meeting_repository.py`)

- `test_create_and_get`
- `test_hash_exists`
- `test_list_for_member`
- `test_delete`
- `test_index_and_search_fts`
