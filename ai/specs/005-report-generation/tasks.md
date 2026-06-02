# 005 — Generación de Reports: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Entidad `Report` (periodo, modo, versión, status, schema_valid…)
- [ ] Entidad `ActionItem`, `KeyTheme`, `Sentiment`, `SentimentPoint`
- [ ] Use case `GenerateReportLLM` — recopila transcripciones, envía a LLM, valida, guarda
- [ ] Use case `PrepareAIContext` — genera `context_for_ai.md` en staging dir
- [ ] Use case `ImportReportFromStaging` — valida, preview, mueve, genera exports y charts
- [ ] Use case `DetectImportedReports` — detecta en rescan
- [ ] Use case `ValidateReportSchema` — valida `content.json` contra schema
- [ ] Use case `GenerateReportCharts` — genera PNGs con Plotly + Kaleido
- [ ] Use case `GenerateReportExports` — genera `report.md` y `report.pdf`
- [ ] Port `LLMPort` — interfaz `generate(prompt) → str`
- [ ] Port `ReportRepository` — interfaz CRUD
- [ ] Port `ReportWriterPort` — interfaz para escritura atómica del report
- [ ] Tests unitarios de todos los use cases

## Adapters

- [ ] `adapters/db/report_repo.py` — implementa `ReportRepository`
- [ ] `adapters/llm/anthropic.py` — implementa `LLMPort` con API Anthropic
- [ ] `adapters/llm/openai.py` — implementa `LLMPort` con API OpenAI
- [ ] `adapters/llm/ollama.py` — implementa `LLMPort` con Ollama local
- [ ] `adapters/charts/sentiment.py` — gráfico evolución de sentiment
- [ ] `adapters/charts/action_items.py` — gráfico evolución de action items
- [ ] `adapters/charts/themes.py` — gráfico frecuencia de temas
- [ ] `adapters/exporters/markdown.py` — genera `report.md` desde `content.json` + Jinja2
- [ ] `adapters/exporters/pdf.py` — genera `report.pdf` (WeasyPrint)
- [ ] Plantilla `llm_prompt.j2` y `context_for_ai.md.j2`
- [ ] `content.schema.json` en raíz del proyecto

## UI

- [ ] Modal "Generar report" (modo LLM): periodo, proveedor, confirmación cloud
- [ ] Modal "Importar report desde staging": preview del `content.json`, confirmar periodo/versión
- [ ] Botón "Preparar contexto para IA" en vista de miembro
- [ ] Barra de progreso durante generación LLM
- [ ] Popup de errores de schema con rutas de campo

## Tests

- [ ] Test unitario: `GenerateReportLLM` (LLM port mockeado, FS port mockeado)
- [ ] Test unitario: `ImportReportFromStaging` — validación, movimiento atómico
- [ ] Test unitario: `ValidateReportSchema` — JSON válido, campos ausentes, tipos incorrectos
- [ ] Test unitario: `GenerateReportCharts` (Kaleido mockeado)
- [ ] Test integración: `ReportRepository` contra SQLite en memoria
- [ ] Test integración: `anthropic.py` / `openai.py` (mock HTTP)
