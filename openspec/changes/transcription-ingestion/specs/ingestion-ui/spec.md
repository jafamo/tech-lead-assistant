# Spec: UI — Ingesta de transcripciones

## Integración en `/team/{slug}`

La página de detalle del miembro (actualmente stub) se amplía con:

1. **Sección "Transcripciones"** — listado de reuniones del miembro (fecha, tipo, título)
2. **Botón "Subir transcripción"** — abre el modal de ingesta
3. **Botón "Editar"** por cada fila — abre el editor inline
4. **Botón "Eliminar"** por cada fila — confirmación + delete

## Modal de ingesta (`ui.dialog`)

```
┌─────────────────────────────────────────────┐
│  Subir transcripción                        │
│                                             │
│  [ Drag & drop o seleccionar fichero(s) ]   │
│  Formatos: .txt .md .vtt .srt               │
│                                             │
│  Tipo de reunión: [dropdown]                │
│  Fecha:          [date input]  (auto)       │
│  Título:         [input]       (opcional)   │
│                                             │
│  ── Ficheros seleccionados ──               │
│  • 2024-03-15.transcript.txt   ✓ / ✗        │
│  • reunion.md                  ✓ / ✗        │
│                                             │
│         [Cancelar]   [Subir todo]           │
└─────────────────────────────────────────────┘
```

- **Auto-detección de fecha**: si el nombre sigue `YYYY-MM-DD*`, se pre-rellena el date input
- **Upload en lote**: se procesa cada fichero en secuencia; errores por fichero (duplicado, formato) se muestran inline sin detener los demás
- **Feedback**: spinner por fichero, toast "N ficheros subidos" al final

## Editor inline (`ui.dialog`)

```
┌─────────────────────────────────────────────┐
│  Editar transcripción — 2024-03-15          │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  <contenido editable>               │   │
│  │  ...                                │   │
│  └─────────────────────────────────────┘   │
│                                             │
│         [Cancelar]   [Guardar]              │
└─────────────────────────────────────────────┘
```

- `ui.textarea` con `rows=20`
- Al guardar: llama `fs.write_transcript_text` + re-indexa FTS

## NiceGUI file upload

Usa `ui.upload` con `multiple=True`, `accept=".txt,.md,.vtt,.srt"`.  
El handler recibe `e: UploadEventArguments` con `e.name`, `e.content` (BytesIO).
