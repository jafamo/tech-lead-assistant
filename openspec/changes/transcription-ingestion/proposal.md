# Proposal: 004 — Ingesta de Transcripciones

## Objetivo

Permitir subir ficheros de transcripción (`.txt`, `.md`, `.vtt`, `.srt`) a `data_root`, con metadatos de reunión, indexación en SQLite y FTS5, detección de duplicados y edición básica desde la UI.

## Contexto

Es el dato de entrada de todo el flujo de valor: sin transcripciones no hay reports. Depende de 003 (necesita TeamMember con slug y tipo de reunión).

## Alcance

### Incluido

- **Domain**: entidad `Meeting`, port `MeetingRepository`, use cases `IngestTranscription`, `ListMeetings`, `GetMeeting`, `DeleteMeeting`, `SearchMeetings`
- **FS**: use case `TranscriptionFileSystem` — copia atómica, nombre canónico, detección de duplicados por hash
- **FTS**: indexación en `search_index` al ingestar; búsqueda con `MATCH`
- **DB adapter**: `SQLMeetingRepository`
- **UI**: modal de subida en `/team/{slug}` (drag-and-drop + file picker), selector de tipo/fecha/participantes, upload en lote, editor de texto inline, listado de reuniones en detalle del miembro

### Excluido

- Reuniones multi-participante (`_shared/meetings/`) → complejidad extra, v2
- Subida de notas `.notes.md` independiente → se hace junto con la transcripción en mismo modal

## Decisiones de diseño

1. **Nombre canónico**: `{data_root}/{slug}/{tipo}/YYYY-MM-DD.transcript.{ext}` — la fecha viene del nombre del fichero si sigue `YYYY-MM-DD*`, si no se pide al usuario.
2. **Hash MD5** del contenido para detectar duplicados antes de copiar. Si ya existe mismo hash → error `DuplicateTranscriptionError`.
3. **FTS5 indexado al ingestar**: el use case llama al repo que inserta en `search_index`. Contenido truncado a 100 KB para no saturar el índice.
4. **Formatos aceptados**: `.txt`, `.md`, `.vtt`, `.srt`. El contenido se almacena tal cual; el parsing de VTT/SRT para extraer texto limpio es opcional en v1.
5. **Edición inline**: `ui.textarea` con el contenido actual; al guardar se reescribe el fichero atómicamente y se re-indexa en FTS.
