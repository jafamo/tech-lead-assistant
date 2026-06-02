Crea la estructura de directorios y el perfil inicial de un nuevo miembro del equipo en data_root.

## Pasos

1. **Obtener parámetros** — si no se han proporcionado, pregunta:
   - Nombre completo del miembro (ej. "María López")
   - Rol / cargo (ej. "Backend Engineer")
   - `data_root` — lee de `.env` o pregunta al usuario

2. **Generar el slug**
   - Lowercase, sin tildes, espacios → guiones
   - Ej: "María López" → `maria-lopez`
   - Si ya existe una carpeta con ese slug, añade sufijo numérico: `maria-lopez-2`

3. **Crear la estructura de directorios**
   ```
   {data_root}/{slug}/
     profile/
     oneToOne/
     seguimiento/
     feedback/
     tecnica/
     retro/
     notes/
     reports/
   ```

4. **Crear `profile.md`** en `{data_root}/{slug}/profile/profile.md`:
   ```markdown
   # {Nombre completo}

   **Rol**: {rol}
   **Slug**: {slug}
   **Fecha de inicio**: {hoy en YYYY-MM-DD}

   ## Contexto

   <!-- Añade aquí notas sobre el miembro: áreas de expertise, objetivos, contexto del equipo -->

   ## Historial de equipo

   <!-- Proyectos anteriores, transfers, cambios de rol -->
   ```

5. **Confirmar al usuario**
   - Muestra el slug generado y la ruta completa creada
   - Recuerda que la app detectará al nuevo miembro la próxima vez que haga rescan
   - Sugiere editar `profile.md` para añadir contexto antes de la primera reunión
