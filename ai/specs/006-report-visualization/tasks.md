# 006 — Visualización y Exportación: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Use case `GetReport` — carga `content.json` + metadatos BD
- [ ] Use case `CompareReports` — genera diff estructurado entre 2 reports
- [ ] Use case `ExportReport` — exporta a PDF, MD o CSV en ruta arbitraria
- [ ] Use case `ExportReportBatch` — exporta múltiples reports
- [ ] Use case `ListReports` — cross-team con filtros
- [ ] Port `ReportExporterPort` — interfaz para exportación
- [ ] Tests unitarios de todos los use cases

## Adapters

- [ ] `adapters/exporters/csv.py` — action items y themes a CSV tabular
- [ ] `adapters/exporters/pdf.py` — comparación como PDF (Jinja2 → HTML → WeasyPrint)
- [ ] Plantillas Jinja2: `report.md.j2`, `report.html.j2`, `comparison.html.j2`

## UI

- [ ] `adapters/ui/pages/report_view.py` — vista de report con todas las secciones
  - [ ] Sección resumen
  - [ ] Sección key themes con badges de frecuencia
  - [ ] Sección action items (open / closed) con fechas
  - [ ] Sección growth signals y riesgos
  - [ ] Gráfico Plotly interactivo de sentiment (color del miembro)
  - [ ] Sección highlights y next 1:1 brief
  - [ ] Advertencia prominente si `schema_valid = false`
  - [ ] Botón "Abrir carpeta" (abre en explorador del SO)
- [ ] `adapters/ui/pages/report_compare.py` — diff lado a lado + gráficos comparativos
- [ ] `adapters/ui/pages/reports_list.py` — listado cross-team con filtros y badges
- [ ] Diálogo de exportación (PDF / MD / CSV / ruta destino)
- [ ] Exportación en lote (selección múltiple)

## Tests

- [ ] Test unitario: `CompareReports`
- [ ] Test unitario: `ExportReport` — cada formato
- [ ] Test unitario: `ListReports` — filtros aplicados correctamente
- [ ] Test integración: `pdf.py` — genera PDF válido
