## 1. Domain — Entidad y excepciones

- [ ] 1.1 Crear `domain/entities/meeting.py` — dataclass `Meeting`
- [ ] 1.2 Añadir a `domain/exceptions.py`: `DuplicateTranscriptionError`, `UnsupportedFileFormatError`, `MeetingNotFoundError`

## 2. Domain — Ports

- [ ] 2.1 Crear `domain/ports/meeting_repository.py` — ABC `MeetingRepository`
- [ ] 2.2 Crear `domain/ports/transcription_fs.py` — ABC `TranscriptionFileSystemPort`

## 3. Domain — Use cases

- [ ] 3.1 `use_cases/ingest_transcription.py` — `IngestTranscription`: hash, validación ext, escritura FS, repo + FTS
- [ ] 3.2 `use_cases/list_meetings.py` — `ListMeetings`: por member_id, ordenados desc
- [ ] 3.3 `use_cases/get_meeting.py` — `GetMeeting`: por id
- [ ] 3.4 `use_cases/delete_meeting.py` — `DeleteMeeting`: elimina fichero + BD + FTS
- [ ] 3.5 `use_cases/search_meetings.py` — `SearchMeetings`: FTS5 query

## 4. Domain — Tests unitarios

- [ ] 4.1 `tests/unit/domain/use_cases/test_ingest_transcription.py` — éxito, duplicado, formato inválido
- [ ] 4.2 `tests/unit/domain/use_cases/test_list_meetings.py` — lista vacía, con resultados
- [ ] 4.3 `tests/unit/domain/use_cases/test_delete_meeting.py` — éxito, not found
- [ ] 4.4 `tests/unit/domain/use_cases/test_search_meetings.py` — con resultados, sin resultados

## 5. FS Adapter

- [ ] 5.1 Crear `adapters/fs/transcription_fs.py` — `LocalTranscriptionFileSystem`

## 6. DB Adapter

- [ ] 6.1 Crear `adapters/db/meeting_repo.py` — `SQLMeetingRepository`
- [ ] 6.2 `tests/integration/test_meeting_repository.py` — 5 tests (create, hash_exists, list, delete, FTS)

## 7. UI — Ampliar `/team/{slug}`

- [ ] 7.1 Sección "Transcripciones" — tabla con fecha, tipo, título, botones editar/eliminar
- [ ] 7.2 Modal "Subir transcripción" — `ui.upload` multi-fichero, selector tipo/fecha/título
- [ ] 7.3 Auto-detección de fecha desde nombre de fichero
- [ ] 7.4 Upload en lote con feedback por fichero (errores inline, toast final)
- [ ] 7.5 Modal "Editar transcripción" — `ui.textarea`, guardar reescribe + re-indexa FTS
- [ ] 7.6 Confirmación "Eliminar transcripción"
