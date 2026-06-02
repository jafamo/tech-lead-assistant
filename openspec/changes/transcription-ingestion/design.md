# Design: 004 — Ingesta de Transcripciones

## Capas afectadas

| Capa | Ficheros nuevos / modificados |
|---|---|
| Domain entity | `domain/entities/meeting.py` |
| Domain exceptions | `domain/exceptions.py` (+3 clases) |
| Domain port | `domain/ports/meeting_repository.py`, `domain/ports/transcription_fs.py` |
| Domain use cases | `domain/use_cases/ingest_transcription.py`, `list_meetings.py`, `get_meeting.py`, `delete_meeting.py`, `search_meetings.py` |
| FS adapter | `adapters/fs/transcription_fs.py` |
| DB adapter | `adapters/db/meeting_repo.py` |
| UI | `adapters/ui/pages/team_detail.py` (ampliar stub) |
| Tests unitarios | `tests/unit/domain/use_cases/test_ingest_transcription.py`, etc. |
| Tests integración | `tests/integration/test_meeting_repository.py` |

## Flujo IngestTranscription

```
UI upload modal
  → IngestTranscription(repo, fs, data_root).execute(member_id, type_id, date, content, filename, title)
      → ext = Path(filename).suffix.lower()
      → si ext no en ALLOWED_EXTENSIONS → UnsupportedFileFormatError
      → file_hash = md5(content)
      → si repo.hash_exists(file_hash) → DuplicateTranscriptionError
      → rel_path = fs.write_transcript(data_root, slug, type_slug, date, ext, content)
      → meeting = repo.create(member_id, type_id, date, rel_path, file_hash, title)
      → content_text = content.decode("utf-8", errors="replace")
      → repo.index_fts(meeting.id, content_text, slug, type_slug)
      → return meeting
```

## Resolución de IDs vs slugs

El use case recibe `team_member_id` e `meeting_type_id` (enteros, desde la BD). La entidad de dominio `Meeting` expone `team_member_slug` y `meeting_type_slug` para que la UI pueda construir rutas sin nuevas consultas.

## FTS — nota de implementación

`search_index` es una tabla virtual FTS5 ya creada en `init_db`. El repo hace INSERTs directos con `text()` de SQLAlchemy porque SQLModel no tiene soporte nativo para FTS.

## Extensiones permitidas

```python
ALLOWED_EXTENSIONS = {".txt", ".md", ".vtt", ".srt"}
```
