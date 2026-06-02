# Spec: Domain — entidad Meeting, port y use cases

## Entidad `Meeting` (domain)

```python
@dataclass
class Meeting:
    id: int
    team_member_slug: str
    meeting_type_slug: str   # oneToOne | seguimiento | feedback | tecnica | retro
    meeting_date: date
    title: Optional[str]
    transcript_path: str     # relativo a data_root
    file_hash: str
    notes_path: Optional[str]
    is_shared: bool
    created_at: datetime
    updated_at: datetime
```

## Port `MeetingRepository` (ABC)

```python
class MeetingRepository(ABC):
    def create(self, team_member_id: int, meeting_type_id: int, meeting_date: date,
               transcript_path: str, file_hash: str, title: Optional[str]) -> Meeting: ...
    def get(self, meeting_id: int) -> Optional[Meeting]: ...
    def list_for_member(self, team_member_id: int) -> list[Meeting]: ...
    def hash_exists(self, file_hash: str) -> bool: ...
    def delete(self, meeting_id: int) -> None: ...
    def index_fts(self, meeting_id: int, content: str, member_slug: str, doc_type: str) -> None: ...
    def search_fts(self, query: str, member_slug: Optional[str] = None) -> list[Meeting]: ...
```

## Excepciones (en `domain/exceptions.py`)

```python
class DuplicateTranscriptionError(TLAError): ...
class UnsupportedFileFormatError(TLAError): ...
class MeetingNotFoundError(TLAError): ...
```

## Use cases

### `IngestTranscription`
- Recibe: `team_member_id`, `meeting_type_id`, `meeting_date`, `content: bytes`, `filename: str`, `title: Optional[str]`
- Calcula hash MD5 del contenido
- Si `repo.hash_exists(hash)` → `DuplicateTranscriptionError`
- Valida extensión (`.txt`, `.md`, `.vtt`, `.srt`) → `UnsupportedFileFormatError`
- Llama `fs.write_transcript(data_root, slug, meeting_type_slug, meeting_date, ext, content)`
- Llama `repo.create(...)` → `Meeting`
- Llama `repo.index_fts(meeting.id, content_text, slug, meeting_type_slug)`
- Devuelve `Meeting`

### `ListMeetings`
- Recibe: `team_member_id`
- Devuelve `list[Meeting]` ordenados por `meeting_date` desc

### `GetMeeting`
- Recibe: `meeting_id`
- Devuelve `Meeting` o `MeetingNotFoundError`

### `DeleteMeeting`
- Recibe: `meeting_id`, `data_root`
- Elimina fichero de disco (si existe)
- Elimina de BD y FTS
- Excepción: `MeetingNotFoundError`

### `SearchMeetings`
- Recibe: `query: str`, `member_slug: Optional[str]`
- Llama `repo.search_fts(query, member_slug)`
- Devuelve `list[Meeting]`
