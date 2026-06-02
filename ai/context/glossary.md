# Glosario

| Término | Definición |
|---|---|
| **data_root** | Directorio raíz donde viven los datos del usuario (personas, transcripciones, reports). Configurable en `.env`. Puede ser local o red. |
| **slug** | Identificador normalizado de una persona: lowercase, sin tildes, espacios → guiones. Ej: `maria-lopez`. |
| **report** | Documento estructurado (`content.json`) que resume un periodo de reuniones con una persona. |
| **content.json** | Fichero JSON con el contenido estructurado de un report. Conforme al JSON schema publicado. |
| **modo llm** | Report generado internamente por la app llamando a un LLM (Anthropic, OpenAI, Ollama). |
| **modo manual** | Report preparado externamente por el usuario (con IA) y depositado en el staging dir para importación. |
| **modo imported** | Report cuyo `content.json` apareció directamente en `data_root/{slug}/reports/` y fue detectado por rescan. |
| **staging dir** | `TLA_REPORTS_IMPORT_DIR`. Directorio intermedio donde el usuario deposita reports antes de importarlos. |
| **rescan** | Proceso que lee el filesystem y reconstruye/actualiza el índice SQLite. |
| **índice** | Base de datos SQLite local que cachea metadata del filesystem para búsqueda rápida y relaciones. Es derivable. |
| **meeting type** | Categoría de reunión: `oneToOne`, `seguimiento`, `feedback`, `tecnica`, `retro`. |
| **action item** | Tarea o compromiso extraído de una reunión, con owner (member o tech_lead) y estado (open/closed). |
| **sentiment** | Lectura del estado emocional/motivacional de una persona. Score de -1 a 1. |
| **key theme** | Tema recurrente detectado en las reuniones de un periodo. |
| **charts** | Gráficos PNG generados con Plotly + Kaleido, almacenados en la carpeta del report. |
| **AGENTS.md** | Fichero en `data_root` que describe las convenciones para que herramientas externas operen sobre los datos. |
| **FDE** | Full Disk Encryption del sistema operativo (BitLocker, LUKS, FileVault). |
| **lock-screen** | Pantalla de login de la app. No cifra datos; solo bloquea la UI. |
| **archivado** | Miembro marcado como inactivo. Su carpeta se mueve a `_archive/`. Se puede reactivar. |
