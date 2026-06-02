Valida un fichero `content.json` de TLA contra el schema oficial.

## Pasos

1. **Obtener la ruta** del `content.json` a validar.
   - Si se pasó como argumento, úsala directamente.
   - Si no, busca `content.json` en el directorio actual o pregunta al usuario.

2. **Leer el schema** desde `content.schema.json` (raíz del proyecto).

3. **Validar la estructura** comprobando:
   - JSON bien formado (sintaxis correcta)
   - Campos obligatorios presentes: `metadata` y `content`
   - `metadata.team_member_slug` — string no vacío
   - `metadata.period_start` y `period_end` — formato `YYYY-MM-DD`
   - `metadata.generation_mode` — uno de `llm`, `manual`, `imported`
   - `metadata.version` — entero positivo
   - `content.summary` — string no vacío
   - `content.action_items.open` y `closed` — arrays (pueden estar vacíos)
   - `content.sentiment.overall` — uno de `positive`, `neutral`, `negative`
   - `content.sentiment.evolution` — array con objetos `{date, score}` donde score ∈ [-1, 1]

4. **Mostrar resultado**:
   - ✅ Sin errores: "content.json válido — listo para importar."
   - ❌ Con errores: lista cada error con la ruta JSON del campo problemático (ej. `content.sentiment.evolution[0].score`)

5. **Si hay errores**, ofrece corregirlos automáticamente cuando sea posible (valores fuera de rango, formato de fecha incorrecto, campo ausente con valor default claro).
