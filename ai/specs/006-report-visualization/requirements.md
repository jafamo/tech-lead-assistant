# 006 — Visualización y Exportación de Reports

**Prioridad**: 6 (mostrar el valor generado en 005)
**Rama**: `feature/006-report-visualization`
**Depende de**: 005-report-generation

## Descripción

Visualización detallada de un report individual, comparación entre dos reports del mismo miembro, y exportación a múltiples formatos.

## Requisitos funcionales

### Visualización (§6.9)
- **RF-VIS-1**: Secciones diferenciadas en la vista del report:
  - Resumen ejecutivo (`summary`)
  - Temas clave (`key_themes`) con frecuencia y evolución
  - Action items: abiertos y cerrados (con fechas)
  - Growth signals
  - Riesgos y preocupaciones
  - Gráfico de sentiment (Plotly interactivo, color del miembro)
  - Highlights
  - Brief para la próxima 1:1
- **RF-VIS-2**: Plotly interactivo con el color asignado al miembro.
- **RF-VIS-3**: Si `schema_valid = false` → advertencia prominente con lista de errores y campos parciales visibles.
- **RF-VIS-4**: Botón "Abrir carpeta" → abre el directorio del report en el explorador de archivos del SO.
- **RF-VIS-5**: Fechas visibles: periodo analizado, fecha de creación, última edición, versión, modo.

### Comparación de reports (§6.7)
- **RF-CMP-1**: Seleccionar 2 reports del mismo miembro → vista diff lado a lado.
- **RF-CMP-2**: Diff por sección con gráficos comparativos (evolución de sentiment entre periodos, variación de action items).
- **RF-CMP-3**: Exportar comparación como PDF.

### Exportación (§6.8)
- **RF-EXP-1**: PDF (Jinja2 → HTML → WeasyPrint).
- **RF-EXP-2**: Markdown (ya generado como `report.md` en la carpeta).
- **RF-EXP-3**: CSV (action items y themes tabulares).
- **RF-EXP-4**: Botón "Exportar a…" → diálogo de guardado en ubicación arbitraria.
- **RF-EXP-5**: Exportación en lote (varios reports a la vez).

### Listado de reports (§6.13)
- **RF-REPS-1**: Página "Reports" — listado cross-team de todos los reports.
- **RF-REPS-2**: Columnas: color dot, persona, periodo, versión, modo (icono), estado, validez, creado, actualizado.
- **RF-REPS-3**: Filtros: persona, periodo, modo, estado, validez.
- **RF-REPS-4**: Acciones por fila: Ver, Exportar. Comparar (cuando exactamente 2 seleccionados).
- **RF-REPS-5**: Badges visuales: `imported` con icono especial; `schema_valid = false` con icono de warning en rojo.

## Casos de uso relacionados

- UC3: Comparar reports trimestrales para performance review.
- UC5: Exportar report a PDF.
- UC10: Ver último report desde Inicio con un click.
