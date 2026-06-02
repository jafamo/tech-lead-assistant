# 004 — Ingesta de Transcripciones

**Prioridad**: 4 (dato de entrada para los reports)
**Rama**: `feature/004-transcription-ingestion`
**Depende de**: 001-bootstrap, 002-authentication, 003-team-management

## Descripción

Subida de ficheros de transcripción a la estructura de `data_root`, con indexación en SQLite y FTS para búsqueda posterior.

## Requisitos funcionales

Extraídos de §6.3 de la spec:

- **RF-TR-1**: Drag-and-drop o file picker para subir ficheros.
- **RF-TR-2**: Formatos aceptados: `.txt`, `.md`, `.vtt`, `.srt`.
- **RF-TR-3**: Al subir: seleccionar tipo de reunión (`oneToOne`, `seguimiento`, `feedback`, `tecnica`, `retro`), fecha (auto-detectada del nombre si sigue `YYYY-MM-DD`, editable), participantes, título opcional.
- **RF-TR-4**: Copia atómica al directorio correcto: `{TLA_DATA_ROOT}/{slug}/{tipo}/YYYY-MM-DD.transcript.{ext}`.
- **RF-TR-5**: Indexación en SQLite (`meeting` + `meeting_participant`) y FTS5 (`search_index`).
- **RF-TR-6**: Upload en lote (múltiples ficheros a la vez, para el mismo miembro).
- **RF-TR-7**: Edición del contenido de la transcripción desde la UI (editor de texto básico).
- **RF-TR-8**: Registrar `created_at` e `imported_at` en el índice. Calcular `file_hash` para detectar duplicados.

## Convenciones del filesystem

- Transcripción: `YYYY-MM-DD.transcript.{ext}`
- Notas asociadas (opcional): `YYYY-MM-DD.notes.md`
- Reuniones multi-participante: `_shared/meetings/{fecha}_{slug}/transcript.{ext}` + `participants.json`

## Casos de uso relacionados

- UC1: Subir transcripción → generar report.
- UC2: Subir transcripción → preparar report externamente.
- UC4: Detectar tema recurrente en ≥3 1:1s (depende de FTS).
- UC11: Claude Code puede depositar ficheros directamente en `data_root`.

## Requisitos no funcionales

- FTS < 300 ms para corpus ≤ 200 reuniones.
- Duplicados detectados por `file_hash` antes de copiar.
- Copia siempre atómica (write-temp + rename).
