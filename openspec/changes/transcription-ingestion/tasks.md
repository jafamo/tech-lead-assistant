## 1. Domain — Entidad y excepciones

- [x] 1.1 Crear `domain/entities/meeting.py` — dataclass `Meeting`
- [x] 1.2 Añadir a `domain/exceptions.py`: `DuplicateTranscriptionError`, `UnsupportedFileFormatError`, `MeetingNotFoundError`

## 2. Domain — Ports

- [x] 2.1 Crear `domain/ports/meeting_repository.py` — ABC `MeetingRepository`
- [x] 2.2 Crear `domain/ports/transcription_fs.py` — ABC `TranscriptionFileSystemPort`

## 3. Domain — Use cases

- [x] 3.1 `use_cases/ingest_transcription.py` — `IngestTranscription`: hash, validación ext, escritura FS, repo + FTS
- [x] 3.2 `use_cases/list_meetings.py` — `ListMeetings`: por member_id, ordenados desc
- [x] 3.3 `use_cases/get_meeting.py` — `GetMeeting`: por id
- [x] 3.4 `use_cases/delete_meeting.py` — `DeleteMeeting`: elimina fichero + BD + FTS
- [x] 3.5 `use_cases/search_meetings.py` — `SearchMeetings`: FTS5 query

## 4. Domain — Tests unitarios

- [x] 4.1 `tests/unit/domain/use_cases/test_ingest_transcription.py` — éxito, duplicado, formato inválido
- [x] 4.2 `tests/unit/domain/use_cases/test_list_meetings.py` — lista vacía, con resultados
- [x] 4.3 `tests/unit/domain/use_cases/test_delete_meeting.py` — éxito, not found
- [x] 4.4 `tests/unit/domain/use_cases/test_search_meetings.py` — con resultados, sin resultados, filtro miembro

## 5. FS Adapter

- [x] 5.1 Crear `adapters/fs/transcription_fs.py` — `LocalTranscriptionFileSystem`

## 6. DB Adapter

- [x] 6.1 Crear `adapters/db/meeting_repo.py` — `SQLMeetingRepository`
- [x] 6.2 `tests/integration/test_meeting_repository.py` — 5 tests (create, hash_exists, list, delete, FTS)

## 7. UI — Ampliar `/team/{slug}`

- [x] 7.1 Sección "Transcripciones" — tabla con fecha, tipo, título, botones editar/eliminar
- [x] 7.2 Modal "Subir transcripción" — `ui.upload` multi-fichero, selector tipo/fecha/título
- [x] 7.3 Auto-detección de fecha desde nombre de fichero
- [x] 7.4 Upload en lote con feedback por fichero (errores inline, toast final)
- [x] 7.5 Modal "Editar transcripción" — `ui.textarea`, guardar reescribe + re-indexa FTS
- [x] 7.6 Confirmación "Eliminar transcripción"
