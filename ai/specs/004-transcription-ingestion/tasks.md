# 004 — Ingesta de Transcripciones: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Entidad `Meeting` (tipo, fecha, transcript_path, notes_path, is_shared, file_hash…)
- [ ] Entidad `MeetingType` (slug, display_name, icon)
- [ ] Use case `IngestTranscript` — valida formato, copia atómica, indexa en BD y FTS
- [ ] Use case `IngestTranscriptBatch` — múltiples ficheros en lote
- [ ] Use case `ListMeetings` — por miembro, por tipo, por rango de fechas
- [ ] Use case `EditTranscript` — actualiza contenido y re-indexa FTS
- [ ] Port `MeetingRepository` — interfaz CRUD
- [ ] Port `FullTextSearchPort` — interfaz para indexar y buscar en FTS
- [ ] Tests unitarios de todos los use cases

## Adapters

- [ ] `adapters/db/meeting_repo.py` — implementa `MeetingRepository`
- [ ] `adapters/db/fts.py` — indexación y búsqueda FTS5
- [ ] `adapters/fs/transcript_ingester.py` — detección de fecha en nombre, copia atómica
- [ ] Detección de duplicados por `file_hash` antes de copiar

## UI

- [ ] Componente drag-and-drop / file picker en vista de miembro
- [ ] Modal de metadatos al subir: tipo, fecha, participantes, título
- [ ] Upload en lote con barra de progreso
- [ ] Editor de transcripción básico (textarea)
- [ ] Lista de transcripciones en vista de detalle de miembro

## Tests

- [ ] Test unitario: `IngestTranscript` — copia atómica, detección de fecha, hash
- [ ] Test unitario: `IngestTranscriptBatch`
- [ ] Test unitario: `EditTranscript` — re-indexa FTS
- [ ] Test integración: `MeetingRepository` contra SQLite en memoria
- [ ] Test integración: FTS5 — indexar y buscar en < 300 ms
