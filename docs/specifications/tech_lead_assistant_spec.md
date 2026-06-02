# Especificación: Tech Lead Assistant (TLA)

> Documento de especificación para Spec-Driven Development.
> Versión: 0.6 — arquitectura hexagonal, Gitflow, tests unitarios obligatorios.
> Última actualización: 2026-06-02

---

## 1. Visión general

Aplicación de escritorio (NiceGUI sobre Python) que ayuda a un tech lead a gestionar y **visualizar** la memoria estructurada de su equipo (~6 personas) a partir de transcripciones de reuniones.

### Principios arquitectónicos

1. **Filesystem-first**: los datos viven como ficheros planos organizados por persona. La app no reclama propiedad exclusiva.
2. **La app es ante todo un visualizador**. Los reports, estadísticas y datos pueden generarse fuera de la app (con IA u otras herramientas) y la app los consume.
3. **Composability con herramientas externas**: `AGENTS.md`, `templates/` y JSON schema publicados en `data_root`.
4. **Índice local, datos posiblemente remotos**: SQLite siempre local; `data_root`, `TLA_STATS_DIR` y `TLA_REPORTS_IMPORT_DIR` pueden estar en red.
5. **Configuración centralizada en `.env`**: todas las rutas, puertos, credenciales y flags.
6. **Fuente de verdad del proyecto en `ai/`**: agnóstica de herramienta; `.claude/` y `.github/` son adaptadores.
7. **Arquitectura hexagonal (Ports & Adapters)**: el dominio no depende de ningún framework, DB ni UI. Las dependencias apuntan siempre hacia dentro: adapters → ports → domain.
8. **Tests unitarios obligatorios**: todo use case tiene tests en aislamiento total (ports mockeados). Un use case sin test se considera incompleto.

### Modos de creación de reports

- **`llm`**: la app genera el report internamente vía API.
- **`manual`**: el usuario prepara el `content.json` externamente (usando IA) y lo deposita en `TLA_REPORTS_IMPORT_DIR/{slug}/`. La app lo importa.
- **`imported`**: un `content.json` válido apareció directamente en `data_root/{slug}/reports/`. La app lo detecta vía rescan.

**Cross-platform**: Windows 10+ y Linux. macOS best-effort.

---

## 2. Objetivos y no-objetivos

### Objetivos (v1)
- Catálogo de personas con directorio propio, color asignado, archivado/reactivación.
- Ingerir transcripciones y depositarlas en la estructura correcta.
- Visualizar reports con secciones, gráficos y exports.
- Generar reports internamente (modo LLM) o importar desde staging dir (modo manual).
- Detectar reports depositados directamente en `data_root` (modo imported).
- Generar gráficos de seguimiento en cada report (sentiment, action items, themes).
- Versionar, comparar y exportar reports (PDF, CSV, Markdown).
- Calendario interno de reuniones con banner de pendientes.
- Página de Estadísticas como **visor** de ficheros generados por IA externamente.
- Login como lock-screen.
- Sincronización con cambios externos vía rescan.
- Interfaz amigable con iconos y diseño visual.
- Sidebar: Inicio, Reports, Estadísticas, Settings.
- Todas las rutas configurables en `.env`.
- Estructura del repo de código con `ai/` como fuente de verdad.

### No-objetivos (v1)
- Multi-usuario.
- Sincronización cloud gestionada por la app.
- Integración API directa con Google Calendar / Outlook (v1.x).
- Integración con Jira / Linear / GitHub.
- Transcripción de audio.
- Mobile.
- Cifrado de ficheros.
- Plantillas custom de report.
- Análisis semántico cross-member (generado por IA externa).
- Generación de estadísticas dentro de la app (la app las visualiza, no las computa).

---

## 3. Personas y casos de uso

### Persona: el Tech Lead (~6 personas a cargo)

### Casos de uso
- **UC1** — Subir transcripción y generar report con LLM.
- **UC2** — Preparar report externamente con IA → depositarlo en staging dir → importar desde la app.
- **UC3** — Comparar reports trimestrales para performance review.
- **UC4** — Detectar tema recurrente en ≥3 1:1s.
- **UC5** — Exportar report a PDF.
- **UC6** — Archivar miembro que deja el equipo; reactivarlo si vuelve.
- **UC7** — Ver banner de reuniones pendientes esta semana.
- **UC8** — Registrar próxima 1:1 con María en el calendario interno y exportar a .ics.
- **UC9** — Ver estadísticas del equipo generadas por IA (ficheros en `TLA_STATS_DIR`).
- **UC10** — Desde Inicio, ver tabla del personal y generar/importar/ver/exportar report con un click.
- **UC11** — Usar Claude Code sobre `data_root/` con `AGENTS.md` y `templates/` para generar un report.
- **UC12** — Tener `data_root` en unidad de red.

---

## 4. Arquitectura de datos

### 4.1 Directorios principales (todos configurables en `.env`)

| Variable | Propósito | Puede ser red | Default |
|---|---|---|---|
| `TLA_DATA_ROOT` | Datos canónicos (personas, transcripciones, reports) | Sí | `~/Documents/TLA/` |
| `TLA_DB_PATH` | Fichero SQLite de índice | **No** (siempre local) | `~/.local/share/tla/tla.db` |
| `TLA_STATS_DIR` | Estadísticas generadas por IA | Sí | `{TLA_DATA_ROOT}/_stats/` |
| `TLA_STATS_HISTORY_DIR` | Histórico de estadísticas | Sí | `{TLA_STATS_DIR}/history/` |
| `TLA_REPORTS_IMPORT_DIR` | Staging dir para reports creados externamente | Sí | `{TLA_DATA_ROOT}/_import/` |
| `TLA_LOG_DIR` | Logs de la app | No | `~/.local/share/tla/logs/` |

### 4.2 Estructura de `data_root`

```
{TLA_DATA_ROOT}/
  AGENTS.md
  README.md
  templates/
    README.md
    content.example.json
    content.guide.md
    profile.example.md
    notes.example.md
    participants.example.json
  _published_schema/
    content.schema.json
  _import/                             # TLA_REPORTS_IMPORT_DIR (default)
    pepe-garcia/
      content.json                     # report preparado externamente, listo para importar
    maria-lopez/
      content.json
  _stats/                              # TLA_STATS_DIR (default)
    current/
      team_overview.json
      team_overview.md
      per_member/
        pepe-garcia.json
        maria-lopez.json
      charts/
        ...
    history/                           # TLA_STATS_HISTORY_DIR (default)
      2026-Q1/
        team_overview.json
        per_member/
          ...
      2026-Q2/
        ...
  _archive/                            # miembros archivados
    ex-miembro-slug/
      ... (misma estructura que un miembro activo)
  pepe-garcia/
    profile/
      profile.md
    oneToOne/
      2026-05-11.transcript.vtt
      2026-05-11.notes.md
    seguimiento/
      ...
    feedback/
      ...
    tecnica/
      ...
    retro/
      ...
    notes/
      2026-05-13.md
    reports/
      2026-05_v1_llm/
        content.json
        report.md
        report.pdf
        charts/
          sentiment_evolution.png
          action_items_evolution.png
          themes_frequency.png
      2026-05_v2_manual/
        content.json
        report.md
        report.pdf
        charts/
          ...
  maria-lopez/
    ...
  _shared/
    meetings/
      2026-05-20_retro_squad_a/
        transcript.vtt
        participants.json
        notes.md
```

### 4.3 Estructura de `TLA_REPORTS_IMPORT_DIR` (staging)

```
{TLA_REPORTS_IMPORT_DIR}/
  pepe-garcia/                         # slug del miembro
    content.json                       # report preparado externamente
  maria-lopez/
    content.json
```

**Flujo de importación** (modo `manual`):
1. El usuario prepara `content.json` fuera de la app (con IA: Claude Code, ChatGPT, scripts, etc.).
2. Lo deposita en `{TLA_REPORTS_IMPORT_DIR}/{slug}/content.json`.
3. Desde la app → vista del miembro → "Importar report desde staging".
4. La app lee el `content.json`, valida contra schema, pide al usuario confirmar periodo y versión.
5. Lo mueve (atómico) a `{TLA_DATA_ROOT}/{slug}/reports/{periodo}_v{N}_manual/content.json`.
6. Genera exports (`report.md`, `report.pdf`) y charts.
7. Si el usuario quiere, la app puede proporcionarle las transcripciones y el prompt para generar el `content.json` externamente (ver RF-REP-STAGE).

### 4.4 Estructura de `TLA_STATS_DIR`

Las estadísticas **no las genera la app**. Son ficheros depositados por IA externa (agents, scripts, Claude Code) que la app visualiza.

```
{TLA_STATS_DIR}/
  current/                             # estadísticas vigentes
    team_overview.json                 # métricas agregadas del equipo
    team_overview.md                   # versión legible
    per_member/
      pepe-garcia.json                 # stats individuales
      maria-lopez.json
    charts/
      meetings_by_type.png
      action_items_trend.png
      sentiment_heatmap.png
  history/                             # versiones anteriores (inmutable)
    2026-Q1/
      team_overview.json
      per_member/
        ...
    2026-Q2/
      ...
```

El schema de `team_overview.json` y `per_member/{slug}.json` se definirá cuando se diseñen los agents/prompts de generación. Por ahora, la app intenta renderizar lo que encuentre con tolerancia a campos desconocidos.

### 4.5 Convenciones

- **Slug de persona**: lowercase, sin tildes, espacios → guiones. Colisión → sufijo numérico.
- **Tipos de reunión**: subcarpetas: `oneToOne`, `seguimiento`, `feedback`, `tecnica`, `retro`. Extensible.
- **Transcripción**: `YYYY-MM-DD.transcript.{ext}`.
- **Notas asociadas**: `YYYY-MM-DD.notes.md`.
- **Reports**: `{periodo}_v{N}_{modo}/`.
- **Charts**: dentro de la carpeta del report, en `charts/`.
- **Multi-participante**: `_shared/meetings/{fecha}_{slug}/`.
- **Archivados**: `_archive/{slug}/`.
- **Fechas en todo**: todos los registros de BD y metadatos de ficheros incluyen `created_at`, `updated_at`, `archived_at`, `imported_at` según aplique.

### 4.6 AGENTS.md, templates/ y schema

Sin cambios respecto a v0.4 (ver artefactos adjuntos). Se añade documentación del staging dir y del stats dir en el `AGENTS.md`.

### 4.7 Acceso concurrente

Sin locking. Escrituras atómicas (write-temp + rename). Last-write-wins.

---

## 5. Modelo del índice (SQLite)

```sql
-- ===== Autenticación =====
user (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- ===== Equipo =====
team_member (
  id INTEGER PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  role TEXT,
  start_date DATE,
  notes TEXT,
  color TEXT NOT NULL,                  -- hex color, ej. '#4A90D9'
  status TEXT NOT NULL DEFAULT 'active', -- 'active' | 'archived'
  archived_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_indexed_at TIMESTAMP
)

-- ===== Reuniones =====
meeting_type (
  id INTEGER PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  display_name TEXT NOT NULL,
  icon TEXT,                            -- nombre de icono (ej. 'users', 'message-circle')
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

meeting (
  id INTEGER PRIMARY KEY,
  meeting_type_id INTEGER NOT NULL REFERENCES meeting_type(id),
  meeting_date DATE NOT NULL,
  title TEXT,
  transcript_path TEXT NOT NULL,
  notes_path TEXT,
  is_shared BOOLEAN DEFAULT 0,
  file_hash TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

meeting_participant (
  meeting_id INTEGER NOT NULL REFERENCES meeting(id),
  team_member_id INTEGER NOT NULL REFERENCES team_member(id),
  PRIMARY KEY (meeting_id, team_member_id)
)

-- ===== Reports =====
report (
  id INTEGER PRIMARY KEY,
  team_member_id INTEGER NOT NULL REFERENCES team_member(id),
  period_label TEXT NOT NULL,
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,
  generation_mode TEXT NOT NULL,        -- 'llm' | 'manual' | 'imported'
  llm_provider TEXT,
  llm_model TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  status TEXT NOT NULL DEFAULT 'draft',
  folder_path TEXT NOT NULL,
  content_hash TEXT,
  schema_valid BOOLEAN DEFAULT 1,
  schema_errors TEXT,
  charts_generated BOOLEAN DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT
)

report_meeting (
  report_id INTEGER NOT NULL REFERENCES report(id),
  meeting_id INTEGER NOT NULL REFERENCES meeting(id),
  PRIMARY KEY (report_id, meeting_id)
)

-- ===== Calendario interno =====
scheduled_meeting (
  id INTEGER PRIMARY KEY,
  team_member_id INTEGER REFERENCES team_member(id),  -- NULL si es grupal
  meeting_type_id INTEGER REFERENCES meeting_type(id),
  title TEXT NOT NULL,
  scheduled_date DATE NOT NULL,
  scheduled_time TIME,
  duration_minutes INTEGER DEFAULT 30,
  recurrence TEXT,                      -- 'weekly' | 'biweekly' | 'monthly' | NULL
  recurrence_end_date DATE,
  location TEXT,
  notes TEXT,
  status TEXT NOT NULL DEFAULT 'pending', -- 'pending' | 'completed' | 'cancelled'
  completed_at TIMESTAMP,
  cancelled_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- ===== Búsqueda full-text =====
CREATE VIRTUAL TABLE search_index USING fts5(
  file_path,
  content,
  member_slug,
  doc_type
);
```

### Paleta de colores (12 colores)

```python
MEMBER_COLORS = [
    '#4A90D9',  # azul
    '#E67E22',  # naranja
    '#27AE60',  # verde
    '#8E44AD',  # morado
    '#E74C3C',  # rojo
    '#1ABC9C',  # turquesa
    '#F39C12',  # amarillo
    '#2980B9',  # azul oscuro
    '#D35400',  # naranja oscuro
    '#16A085',  # verde azulado
    '#C0392B',  # rojo oscuro
    '#7F8C8D',  # gris
]
```

Se asigna automáticamente al crear miembro (round-robin); se puede cambiar desde la UI.

---

## 6. Requisitos funcionales

### 6.1 Autenticación
- **RF-AUTH-1**: Primer arranque: crear username + password, elegir `TLA_DATA_ROOT` (o confirmar el del `.env`).
- **RF-AUTH-2**: Lock-screen en arranques posteriores.
- **RF-AUTH-3**: Password hash con bcrypt (cost ≥ 12). No cifra ficheros.
- **RF-AUTH-4**: Retardo exponencial tras 3 intentos fallidos.
- **RF-AUTH-5**: Timeout de inactividad configurable (`TLA_SESSION_TIMEOUT_MIN`).
- **RF-AUTH-6**: Cambio de password en Settings.

### 6.2 Gestión del equipo
- **RF-TEAM-1**: CRUD de team members. Crear genera estructura de directorios + `profile.md` desde plantilla. Asigna color automáticamente.
- **RF-TEAM-2**: Renombrar persona: mueve carpeta al nuevo slug.
- **RF-TEAM-3 (Archivar)**: Botón "Archivar" en la ficha del miembro. Mueve su carpeta de `{TLA_DATA_ROOT}/{slug}/` a `{TLA_DATA_ROOT}/_archive/{slug}/`. Cambia `status` a `archived`, registra `archived_at`. No aparece en la tabla principal de Inicio.
- **RF-TEAM-4 (Reactivar)**: Desde la sección de archivados, botón "Reactivar". Mueve la carpeta de vuelta a `{TLA_DATA_ROOT}/{slug}/`. Cambia `status` a `active`, limpia `archived_at`.
- **RF-TEAM-5 (Sección archivados)**: Accesible desde Inicio con link "Ver archivados (N)" bajo la tabla principal. Tabla con mismo formato pero con botones "Reactivar" y "Ver historial".
- **RF-TEAM-6**: Cambiar color del miembro desde la UI.
- **RF-TEAM-7**: Listado con búsqueda, filtros y ordenación.
- **RF-TEAM-8**: Vista de detalle por persona con timeline, color como acento visual, todas las fechas visibles.

### 6.3 Ingesta de transcripciones
- **RF-TR-1**: Drag-and-drop o file picker.
- **RF-TR-2**: Formatos: `.txt`, `.md`, `.vtt`, `.srt`.
- **RF-TR-3**: Al subir: tipo, fecha (auto-detectada), participantes, título opcional.
- **RF-TR-4**: Copia atómica a la ubicación correspondiente.
- **RF-TR-5**: Indexación en SQLite y FTS.
- **RF-TR-6**: Upload en lote.
- **RF-TR-7**: Edición desde la UI.
- **RF-TR-8**: Registrar `created_at` e `imported_at` en el índice.

### 6.4 Reports — tres modos

#### Modo `llm` (generación interna)
- **RF-REP-LLM-1**: Desde la vista del miembro, elegir rango y modo LLM.
- **RF-REP-LLM-2**: Envío de transcripciones al LLM con prompt → `content.json`.
- **RF-REP-LLM-3**: Validación, render de exports y charts.

#### Modo `manual` (import desde staging dir)
- **RF-REP-STAGE-1**: El usuario prepara `content.json` fuera de la app y lo deposita en `{TLA_REPORTS_IMPORT_DIR}/{slug}/content.json`.
- **RF-REP-STAGE-2**: Desde la vista del miembro → "Importar report desde staging". La app busca en `{TLA_REPORTS_IMPORT_DIR}/{slug}/`.
- **RF-REP-STAGE-3**: Preview del contenido + validación contra schema. El usuario confirma periodo y versión.
- **RF-REP-STAGE-4**: La app **mueve** (no copia) el fichero de staging a `{TLA_DATA_ROOT}/{slug}/reports/{periodo}_v{N}_manual/content.json`.
- **RF-REP-STAGE-5**: Genera exports y charts.
- **RF-REP-STAGE-6**: Botón "Preparar contexto para IA" — la app genera un fichero temporal con las transcripciones del rango + el schema + el prompt sugerido, listo para copiar/pegar o pasar a Claude Code. Lo deposita en `{TLA_REPORTS_IMPORT_DIR}/{slug}/context_for_ai.md`.

#### Modo `imported` (detección automática)
- **RF-REP-IMP-1**: En rescan, la app detecta carpetas `*_imported/` en `{TLA_DATA_ROOT}/{slug}/reports/` con `content.json` nuevo.
- **RF-REP-IMP-2**: Valida, indexa, genera exports y charts si faltan.

#### Comunes a todos los modos
- **RF-REP-COM-1**: Report nace como `draft`; finalización explícita.
- **RF-REP-COM-2**: Si JSON inválido contra schema → popup con ruta y errores, report en estado "con errores".
- **RF-REP-COM-3**: Todos los reports registran `created_at`, `updated_at`, `generation_mode`.

### 6.5 Gráficos de seguimiento en cada report
- **RF-CHART-1**: Cada report genera PNGs en `charts/`: `sentiment_evolution.png`, `action_items_evolution.png`, `themes_frequency.png`.
- **RF-CHART-2**: Plotly + Kaleido para PNGs estáticos. Plotly interactivo en UI.
- **RF-CHART-3**: Si Kaleido falla: warning, omitir PNGs, UI sigue con Plotly interactivo. No bloqueante.
- **RF-CHART-4**: Si datos insuficientes para un gráfico, se omite ese gráfico.
- **RF-CHART-5**: Los gráficos usan el color asignado al miembro como color principal.

### 6.6 Versionado e historial
- **RF-VER-1**: Cada generación crea carpeta nueva `_v{N+1}_`.
- **RF-VER-2 (sobrescribir)**: Reemplaza `content.json` de la última versión, regenera exports y charts.
- **RF-VER-3**: Listado de versiones del filesystem con fechas.

### 6.7 Comparación de reports
- **RF-CMP-1**: Seleccionar 2 reports (misma persona) → diff lado a lado.
- **RF-CMP-2**: Diff por sección con gráficos comparativos.
- **RF-CMP-3**: Exportar comparación como PDF.

### 6.8 Exportación
- **RF-EXP-1**: PDF (Jinja2 → HTML → WeasyPrint o alternativa).
- **RF-EXP-2**: Markdown.
- **RF-EXP-3**: CSV (action items y themes tabulares).
- **RF-EXP-4**: Botón "Exportar a..." copia a ubicación arbitraria.
- **RF-EXP-5**: Exportación en lote.

### 6.9 Visualización de un report
- **RF-VIS-1**: Secciones diferenciadas: resumen, themes, action items (open/closed), growth, riesgos, sentiment chart, highlights, next 1:1 brief.
- **RF-VIS-2**: Plotly interactivo con color del miembro.
- **RF-VIS-3**: Si `schema_valid = false`, advertencia con errores y campos parciales.
- **RF-VIS-4**: Botón "Abrir carpeta" abre ruta en filesystem.
- **RF-VIS-5**: Todas las fechas visibles (creación, periodo, última edición).

### 6.10 Calendario interno y banner de pendientes

#### Calendario
- **RF-CAL-1**: Crear reuniones programadas por miembro (1:1, seguimiento, etc.) con fecha, hora, duración.
- **RF-CAL-2**: Soporte de recurrencia: semanal, bi-semanal, mensual.
- **RF-CAL-3**: Marcar reunión como completada (idealmente al subir la transcripción correspondiente).
- **RF-CAL-4**: Cancelar reunión con registro.
- **RF-CAL-5**: Exportar reunión individual o rango a fichero `.ics` para importar en Google Calendar / Outlook.
- **RF-CAL-6**: Vista de lista de próximas reuniones (en vista de miembro y en Inicio).

#### Banner de pendientes (en Inicio)
- **RF-BANNER-1**: Banda visible en la parte superior de Inicio. Icono + texto para cada alerta.
- **RF-BANNER-2**: Tipos de alertas:
  - 🗓️ Reuniones programadas esta semana.
  - ⚠️ Reuniones vencidas (pasadas y no marcadas como completadas/canceladas).
  - 📋 Action items abiertos >30 días (por miembro, con color).
  - 🔄 Temas recurrentes detectados en ≥3 reports recientes.
  - 👤 Miembros sin reunión registrada en >3 semanas.
  - 📥 Reports disponibles en staging dir pendientes de importar.
  - 🔌 `data_root` desconectado (si en red).
- **RF-BANNER-3**: Cada alerta es clickeable: navega a la reunión, miembro o report relevante.
- **RF-BANNER-4**: Número total de alertas visible en el sidebar junto a "Inicio" como badge.

### 6.11 Sidebar de navegación
- **RF-NAV-1**: Sidebar persistente con secciones:
  1. 🏠 **Inicio** (default tras login) — badge con número de alertas.
  2. 📄 **Reports**
  3. 📊 **Estadísticas**
  4. ⚙️ **Settings** (al final, separado visualmente)
- **RF-NAV-2**: Sección activa resaltada.
- **RF-NAV-3**: Sidebar colapsable (sólo iconos cuando colapsado).
- **RF-NAV-4**: Icono + texto en cada item. Diseño visual con color de acento.

### 6.12 Página Inicio
- **RF-HOME-1**: Vista por defecto tras login.
- **RF-HOME-2**: **Banner de pendientes** (ver 6.10).
- **RF-HOME-3**: **Tabla del personal** con columnas:
  - 🎨 Indicador de color del miembro.
  - Nombre.
  - Rol.
  - Última reunión (fecha).
  - Próxima reunión programada (fecha, si hay).
  - Action items abiertos (count).
  - Último report (periodo + modo + fecha).
  - Acciones (botones con iconos por fila):
    - 📝 **Generar report** → modal para elegir modo (LLM) y periodo.
    - 📥 **Importar report** → importar desde staging dir.
    - 👁️ **Ver último report** → navega al report más reciente.
    - 📤 **Exportar último** → diálogo de export (PDF/MD/CSV).
- **RF-HOME-4**: Buscador rápido sobre la tabla.
- **RF-HOME-5**: Link "👥 Ver archivados (N)" bajo la tabla si hay miembros archivados.

### 6.13 Página Reports
- **RF-REPS-1**: Listado cross-team de todos los reports.
- **RF-REPS-2**: Columnas: 🎨 Color, Persona, Periodo, Versión, Modo (icono), Estado, Validez, Creado, Actualizado.
- **RF-REPS-3**: Filtros: persona, periodo, modo, estado, validez.
- **RF-REPS-4**: Acciones: Ver, Exportar, Comparar (cuando 2 seleccionados).
- **RF-REPS-5**: Badges visuales: `imported` con icono, `schema_valid = false` con warning.

### 6.14 Página Estadísticas
La página es un **visor** de ficheros depositados en `TLA_STATS_DIR`. La app no genera las estadísticas.

- **RF-STAT-1**: Lee `{TLA_STATS_DIR}/current/team_overview.json` y muestra su contenido renderizado. Si el fichero no existe, muestra estado vacío con instrucciones.
- **RF-STAT-2**: Lee `{TLA_STATS_DIR}/current/per_member/{slug}.json` para stats individuales.
- **RF-STAT-3**: Muestra las imágenes de `{TLA_STATS_DIR}/current/charts/` si existen.
- **RF-STAT-4**: Selector de periodo histórico: lee desde `{TLA_STATS_HISTORY_DIR}/{periodo}/`.
- **RF-STAT-5**: Si un fichero de stats está malformado, popup con ruta y error.
- **RF-STAT-6**: Botón "Preparar contexto para IA" — genera un fichero temporal con los datos necesarios (reports recientes, action items, etc.) para que el usuario se lo pase a un agente externo que genere las estadísticas. Lo deposita en `{TLA_STATS_DIR}/context_for_ai.md`.
- **RF-STAT-7**: Exportar la vista actual como PDF.
- **RF-STAT-8**: Los schemas de stats se definirán al diseñar los agents/prompts. Por ahora la app renderiza con tolerancia: muestra lo que pueda parsear y omite lo que no.

### 6.15 Página Settings
- **RF-SET-1**: Valores efectivos de `.env` (read-only) con badge del default.
- **RF-SET-2**: Override runtime de settings no sensibles.
- **RF-SET-3**: Cambio de password.
- **RF-SET-4**: Botones: "Rescan", "Regenerar AGENTS.md", "Regenerar templates", "Re-publicar schema".
- **RF-SET-5**: Diagnóstico: estado de conexión a `TLA_DATA_ROOT`, `TLA_STATS_DIR`, `TLA_REPORTS_IMPORT_DIR`; estado de LLM.
- **RF-SET-6**: Gestión de tipos de reunión (añadir/editar el catálogo).

### 6.16 Sincronización (rescan)
- **RF-SYNC-1**: Rescan completo al arrancar (configurable).
- **RF-SYNC-2**: Botón "Rescan" en Settings.
- **RF-SYNC-3**: Red caída → estado "desconectado", deshabilitar escrituras.
- **RF-SYNC-4**: Fichero malformado → popup con ruta y errores.
- **RF-SYNC-5**: Detectar reports nuevos en staging dir → notificar en banner.
- **RF-SYNC-6**: Detectar miembros archivados/reactivados si la operación se hizo desde fuera.

### 6.17 UI y diseño visual
- **RF-UI-1**: Interfaz amigable con iconos en botones, menú, estados y acciones. Usar librería de iconos (Tabler Icons, Material Icons o similar disponible en NiceGUI).
- **RF-UI-2**: Cada miembro identificado visualmente con su color (dot, barra lateral, acento en gráficos).
- **RF-UI-3**: Tooltips en botones de acción.
- **RF-UI-4**: Indicadores de estado visuales (badges, iconos, colores semáforo para alertas).
- **RF-UI-5**: Feedback visual en operaciones (spinners, toasts de confirmación, barras de progreso).
- **RF-UI-6**: Modo oscuro / claro (NiceGUI lo soporta nativamente). Toggle en Settings.
- **RF-UI-7**: Responsive para distintos tamaños de ventana (no mobile, pero sí ventana redimensionada).

### 6.18 AGENTS.md y templates
- **RF-MAINT-1**: Creados al inicializar `data_root` si no existen.
- **RF-MAINT-2**: Regenerados al subir versión del schema (preservar "User notes").
- **RF-MAINT-3**: Schema publicado en `_published_schema/`.

---

## 7. Configuración (`.env`)

```env
# === Server ===
TLA_HOST=127.0.0.1
TLA_PORT=8080

# === Paths — datos ===
TLA_DATA_ROOT=/mnt/nas/TLA
TLA_DB_PATH=                            # vacío = default per-OS (siempre local)

# === Paths — reports import (staging) ===
TLA_REPORTS_IMPORT_DIR=                 # vacío = {TLA_DATA_ROOT}/_import/

# === Paths — estadísticas ===
TLA_STATS_DIR=                          # vacío = {TLA_DATA_ROOT}/_stats/
TLA_STATS_HISTORY_DIR=                  # vacío = {TLA_STATS_DIR}/history/

# === Paths — logs ===
TLA_LOG_DIR=

# === LLM ===
TLA_LLM_PROVIDER=none
TLA_LLM_MODEL=
TLA_ANTHROPIC_API_KEY=
TLA_OPENAI_API_KEY=
TLA_OLLAMA_HOST=http://localhost:11434

# === Sesión ===
TLA_SESSION_TIMEOUT_MIN=30
TLA_LOG_LEVEL=INFO
TLA_LOCALE=es

# === Rescan y red ===
TLA_RESCAN_ON_STARTUP=true
TLA_NETWORK_TIMEOUT_SEC=10
TLA_NETWORK_RETRY_COUNT=2

# === UI ===
TLA_THEME=auto                          # auto | light | dark
```

---

## 8. Requisitos no funcionales

### 8.1 Seguridad
- Login = lock-screen. Ficheros en plano. Recomendar FDE del SO.

### 8.2 Rendimiento
- Arranque <3s local, <10s red.
- Rescan <5s local, <30s red (≤100 ficheros).
- Charts PNG <1s por chart.
- FTS <300ms.

### 8.3 Cross-platform
- Windows 10+, Ubuntu 22.04+, Fedora 38+.
- Soporta SMB/NFS para `TLA_DATA_ROOT`, `TLA_STATS_DIR`, `TLA_REPORTS_IMPORT_DIR`.

### 8.4 Red
- Escrituras atómicas. Timeout configurable. Estado "desconectado" sin crash.

### 8.5 i18n
- v1: español. Preparado para i18n.

### 8.6 Observabilidad
- Logs locales con rotación. Sin telemetría.

### 8.7 Fechas
- Todos los registros incluyen `created_at` y `updated_at` como mínimo.
- Los timestamps se almacenan en UTC en la BD y se muestran en hora local en la UI.
- Los ficheros de datos usan ISO 8601 para fechas y datetimes.

### 8.8 Branching — Gitflow

Ramas permanentes:
- `main` — producción. Solo recibe merges desde `release/*` y `hotfix/*`.
- `develop` — integración. Base de todas las features.

Ramas de soporte:
- `feature/<NNN-nombre>` — nueva funcionalidad. Sale de `develop`, merge a `develop`. El nombre referencia la spec (`feature/001-authentication`).
- `release/<version>` — preparación de release. Sale de `develop`, merge a `main` y `develop`.
- `hotfix/<nombre>` — fix urgente en producción. Sale de `main`, merge a `main` y `develop`.

Commits: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).

### 8.9 Tests

| Nivel | Ubicación | Qué testea | Cobertura mínima |
|---|---|---|---|
| Unitario | `tests/unit/domain/` | Use cases y entities en aislamiento (ports mockeados) | 90% en `domain/` |
| Integración | `tests/integration/` | Adapters contra SQLite en memoria / FS temporal | 70% en `adapters/` |
| E2E | `tests/e2e/` | Flujos completos desde la UI | 60% en `adapters/ui/` |

Regla: un use case sin test unitario se considera incompleto. Los ports siempre se mockean en tests unitarios — ningún test unitario toca DB, filesystem ni red.

---

## 9. Flujos principales

### Flow A — Primera vez
1. Arrancar → "Crear cuenta".
2. Username + password.
3. Confirmar `TLA_DATA_ROOT` del `.env` (o elegir).
4. Banner FDE del SO.
5. Crear `AGENTS.md`, `README.md`, `templates/`, `_published_schema/`, `_import/`, `_stats/`.
6. Inicio con tabla vacía + onboarding.

### Flow B — Generar report con LLM
1. Inicio → fila de María → 📝 "Generar report".
2. Modal: periodo, modo LLM, proveedor.
3. Progreso → `{TLA_DATA_ROOT}/maria-lopez/reports/2026-05_v1_llm/` con todo.
4. Navega al report.

### Flow C — Preparar e importar report manual
1. Desde la app: vista de Pepe → "Preparar contexto para IA".
2. La app genera `{TLA_REPORTS_IMPORT_DIR}/pepe-garcia/context_for_ai.md` con transcripciones + schema + prompt sugerido.
3. El usuario abre Claude Code / ChatGPT, pega el contexto, obtiene `content.json`.
4. Deposita en `{TLA_REPORTS_IMPORT_DIR}/pepe-garcia/content.json`.
5. Desde la app: Inicio → fila de Pepe → 📥 "Importar report".
6. Preview + confirmar periodo y versión.
7. Mueve a `{TLA_DATA_ROOT}/pepe-garcia/reports/2026-05_v1_manual/`. Genera exports y charts.

### Flow D — Archivar miembro
1. Vista de Ana → "Archivar".
2. Confirmación: "¿Archivar a Ana Fernández? Su historial se conservará pero no aparecerá en la tabla principal."
3. Carpeta movida a `_archive/ana-fernandez/`. Status `archived`, `archived_at` registrado.
4. En Inicio: link "Ver archivados (1)".
5. Si Ana vuelve al equipo: "Reactivar" → carpeta vuelve a raíz, status `active`.

### Flow E — Calendario y banner
1. Vista de María → "Programar reunión" → 1:1, próximo martes 10:00, recurrencia bi-semanal.
2. Inicio → banner: "🗓️ 1:1 con María — martes 10:00".
3. Tras la reunión, subir transcripción → la app ofrece marcar la reunión programada como completada.
4. Si pasa la fecha sin marcar como completada → banner: "⚠️ 1:1 con María vencida (martes pasado)".
5. Exportar todas las reuniones de la semana a `.ics` → importar en Google Calendar.

### Flow F — Ver estadísticas
1. Un agente externo genera `team_overview.json` y lo deposita en `{TLA_STATS_DIR}/current/`.
2. Sidebar → Estadísticas.
3. La app renderiza el contenido del JSON + muestra los PNGs de `charts/` si existen.
4. Cambiar a "2026-Q1" → lee de `{TLA_STATS_HISTORY_DIR}/2026-Q1/`.

### Flow G — Fichero malformado
1. Rescan detecta `content.json` inválido.
2. Popup: ruta + errores.
3. Report visible con estado "con errores".

---

## 10. Modos LLM

Sin cambios respecto a v0.4. Proveedores: Anthropic, OpenAI, Ollama. Prompt vía Jinja2. Modal de confirmación para cloud.

---

## 11. Criterios de aceptación del MVP

- [ ] Crear cuenta, confirmar `TLA_DATA_ROOT` del `.env`, login.
- [ ] Crear miembro genera directorios + `profile.md` + asigna color.
- [ ] Archivar miembro mueve a `_archive/`, desaparece de tabla principal. Reactivar lo devuelve.
- [ ] Subir transcripción la copia y la indexa con todas las fechas.
- [ ] Generar report con LLM crea carpeta completa con `content.json`, exports y charts.
- [ ] "Preparar contexto para IA" genera fichero en staging dir.
- [ ] Importar report desde staging dir lo valida, previsualiza, mueve y genera exports/charts.
- [ ] Detectar e indexar reports `imported` en rescan.
- [ ] Visualización de report con secciones, gráficos y color del miembro.
- [ ] Comparación de 2 reports con diff y gráficos.
- [ ] Exportar a PDF, MD, CSV.
- [ ] Popup al detectar fichero malformado.
- [ ] Calendario interno: programar reunión, recurrencia, marcar completada, exportar .ics.
- [ ] Banner de pendientes con todas las alertas listadas en RF-BANNER-2.
- [ ] Página Estadísticas como visor de ficheros de `TLA_STATS_DIR`.
- [ ] Sidebar con Inicio (badge), Reports, Estadísticas, Settings.
- [ ] Tabla del personal con color, fechas, botones de acción por fila.
- [ ] Sección de archivados accesible desde Inicio.
- [ ] Interfaz con iconos, tooltips, toasts, feedback visual.
- [ ] Todas las rutas configurables en `.env` (data, DB, stats, import, logs).
- [ ] `TLA_DB_PATH` respetado; DB siempre local.
- [ ] Funciona con `data_root` en red. Estado "desconectado" si cae.
- [ ] Funciona en Windows 10+ y Ubuntu 22.04+.

---

## 12. Fuera de alcance (v1)

- Multi-usuario.
- Sync cloud.
- API directa con Google Calendar / Outlook (v1.x; v1 exporta .ics).
- Jira / Linear / GitHub.
- Transcripción de audio.
- Mobile.
- Cifrado.
- Generación de estadísticas dentro de la app.
- Análisis semántico cross-member.
- Plantillas custom de report.
- Watcher de filesystem.
- Locking.

---

## 13. Decisiones y asunciones

### Asunciones
- **A1**: Dispositivo de grabación entrega texto, no audio.
- **A2**: Single-user, posiblemente multi-device.
- **A3**: Ficheros en plano, seguridad en FDE del SO.
- **A4**: Volumen ≤6 personas, ≤200 reuniones/año.
- **A5**: La app no reclama propiedad exclusiva.
- **A6**: Las estadísticas las genera IA externa; la app las visualiza.
- **A7**: Los reports "manuales" se preparan externamente con IA.

### Decisiones tomadas
- **D-popup**: Ficheros malformados → popup.
- **D-no-git**: Sin integración git.
- **D-env**: `.env` como config primaria con TODAS las rutas.
- **D-db-local**: SQLite siempre local.
- **D-archive**: Archivado mueve a `_archive/`, reactivación lo devuelve.
- **D-color**: Color por miembro, paleta de 12, round-robin + editable.
- **D-calendar-v1**: Calendario interno + .ics. Sin API externa en v1.
- **D-stats-viewer**: Estadísticas = visor de ficheros externos.
- **D-manual-staging**: Reports manuales = import desde staging dir.

### Pendientes
- **D1**: Motor PDF (WeasyPrint vs pdfkit vs Chromium headless).
- **D2**: ORM (SQLModel vs peewee). Recomendación: SQLModel.
- **D3**: Prompt LLM exacto — iterar con ejemplos reales.
- **D4**: Schema de estadísticas (`team_overview.json`, `per_member/{slug}.json`) — definir al diseñar agents.
- **D5**: Migración de schema de `content.json` cuando evolucione.

---

## 14. Estructura del repositorio de código

```
tla/                                   # raíz del proyecto
│
├── ai/                                # 🧠 fuente de verdad agnóstica de herramienta
│   ├── context/
│   │   ├── architecture.md            # stack, decisiones técnicas
│   │   ├── business.md                # contexto de negocio
│   │   ├── coding-standards.md        # convenciones de código
│   │   └── glossary.md                # términos del dominio
│   │
│   ├── rules/
│   │   ├── backend.md                 # reglas Python/NiceGUI
│   │   ├── security.md               # reglas de seguridad
│   │   └── ui.md                      # reglas de interfaz
│   │
│   ├── prompts/
│   │   ├── report-generation.md       # prompt para generar reports
│   │   ├── stats-generation.md        # prompt para generar estadísticas
│   │   └── code-review.md            # prompt para review de código
│   │
│   └── specs/
│       ├── 001-authentication/
│       │   ├── requirements.md
│       │   ├── design.md
│       │   └── tasks.md
│       ├── 002-team-management/
│       │   ├── requirements.md
│       │   ├── design.md
│       │   └── tasks.md
│       ├── 003-transcription-ingestion/
│       │   └── ...
│       ├── 004-report-generation/
│       │   └── ...
│       ├── 005-report-visualization/
│       │   └── ...
│       ├── 006-calendar-reminders/
│       │   └── ...
│       ├── 007-statistics-viewer/
│       │   └── ...
│       └── 008-settings-rescan/
│           └── ...
│
├── docs/
│   ├── specifications/
│   │   └── tech_lead_assistant_spec.md   # este fichero
│   ├── architecture/
│   └── decisions/
│
├── src/
│   └── tla/
│       ├── __init__.py
│       ├── main.py                    # entrypoint NiceGUI
│       ├── config.py                  # carga .env + defaults
│       ├── auth.py
│       │
│       ├── domain/                    # ── núcleo hexagonal (sin dependencias externas)
│       │   ├── entities/
│       │   │   ├── member.py          # TeamMember, color, status
│       │   │   ├── meeting.py         # Meeting, MeetingType
│       │   │   ├── report.py          # Report, ActionItem, KeyTheme, Sentiment
│       │   │   └── calendar.py        # ScheduledMeeting
│       │   ├── use_cases/
│       │   │   ├── members.py         # ArchiveMember, ReactivateMember, CreateMember…
│       │   │   ├── meetings.py        # IngestTranscript, ListMeetings…
│       │   │   ├── reports.py         # GenerateReport, ImportReport, CompareReports…
│       │   │   ├── calendar.py        # ScheduleMeeting, MarkCompleted, ExportICS…
│       │   │   └── stats.py           # LoadTeamStats, LoadMemberStats…
│       │   ├── ports/
│       │   │   ├── member_repository.py
│       │   │   ├── meeting_repository.py
│       │   │   ├── report_repository.py
│       │   │   ├── calendar_repository.py
│       │   │   ├── llm_port.py        # BaseLLMPort (interfaz)
│       │   │   └── report_writer.py   # ReportWriterPort (interfaz)
│       │   └── exceptions.py          # excepciones de dominio
│       │
│       ├── adapters/                  # ── implementaciones de los ports
│       │   ├── db/
│       │   │   ├── models.py          # SQLModel
│       │   │   ├── fts.py
│       │   │   ├── member_repo.py
│       │   │   ├── meeting_repo.py
│       │   │   ├── report_repo.py
│       │   │   └── calendar_repo.py
│       │   ├── fs/
│       │   │   ├── paths.py
│       │   │   ├── scanner.py
│       │   │   ├── writer.py          # write-temp + rename atómico
│       │   │   ├── agents_md.py
│       │   │   └── templates_publisher.py
│       │   ├── llm/
│       │   │   ├── anthropic.py
│       │   │   ├── openai.py
│       │   │   └── ollama.py
│       │   ├── exporters/
│       │   │   ├── pdf.py
│       │   │   ├── markdown.py
│       │   │   ├── csv.py
│       │   │   └── ics.py
│       │   ├── charts/
│       │   │   ├── renderer.py
│       │   │   ├── sentiment.py
│       │   │   ├── action_items.py
│       │   │   └── themes.py
│       │   └── ui/
│       │       ├── layout/
│       │       │   ├── sidebar.py
│       │       │   └── topbar.py
│       │       ├── pages/
│       │       │   ├── login.py
│       │       │   ├── home.py
│       │       │   ├── reports_list.py
│       │       │   ├── statistics.py
│       │       │   ├── settings.py
│       │       │   ├── member_detail.py
│       │       │   ├── member_archive.py
│       │       │   ├── meeting_new.py
│       │       │   ├── report_view.py
│       │       │   └── report_compare.py
│       │       └── components/
│       │           ├── personnel_table.py
│       │           ├── report_form.py
│       │           ├── sentiment_chart.py
│       │           ├── banner_alerts.py
│       │           ├── calendar_widget.py
│       │           ├── error_popup.py
│       │           ├── color_picker.py
│       │           └── action_buttons.py
│       │
│       └── templates/                 # Jinja2 internos (no confundir con data_root/templates/)
│           ├── report.md.j2
│           ├── report.html.j2
│           ├── llm_prompt.j2
│           ├── context_for_ai.md.j2
│           ├── profile.md.j2
│           ├── AGENTS.md.j2
│           └── README.md.j2
│
├── tests/
│   ├── unit/
│   │   └── domain/
│   │       ├── entities/              # tests de entidades de dominio
│   │       └── use_cases/             # tests de use cases (ports mockeados)
│   ├── integration/                   # adapters contra SQLite en memoria / FS temporal
│   ├── e2e/                           # flujos completos desde la UI
│   └── fixtures/
│       └── sample_data_root/
│
├── .claude/
│   └── CLAUDE.md                      # adaptador para Claude Code
│
├── .github/
│   └── copilot-instructions.md        # adaptador para GitHub Copilot
│
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 15. Dependencias

### Core
```
nicegui>=2.0
plotly>=5.18
pandas>=2.0
jinja2>=3.1
python-dotenv>=1.0
kaleido>=0.2
```

### Recomendadas
```
sqlmodel>=0.0.14
bcrypt>=4.0
weasyprint>=60
markdown-it-py>=3.0
python-slugify>=8.0
pydantic>=2.5
jsonschema>=4.21
icalendar>=5.0              # generación de .ics
```

### Opcionales (LLM)
```
anthropic>=0.30
openai>=1.40
ollama>=0.3
```

---

## 16. Roadmap post-v1

- **v1.x**: Integración API con Google Calendar / Outlook (OAuth).
- **v1.x**: Vault mode (cifrado on-lock).
- **v1.x**: Watcher de filesystem.
- **v1.x**: Transcripción de audio (Whisper local).
- **v2.0**: Multi-usuario con backend remoto.
- **v2.x**: Vista de equipo con análisis semántico cross-member.
- **v2.x**: Integraciones Jira / Linear.
