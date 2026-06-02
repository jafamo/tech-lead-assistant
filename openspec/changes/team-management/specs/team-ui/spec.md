# Spec: UI — páginas de gestión del equipo

## Página `/team` (`adapters/ui/pages/team.py`)

Protegida con `@require_auth`.

### Layout

```
┌─────────────────────────────────────────┐
│  Equipo            [+ Añadir miembro]   │
│  🔍 Buscar por nombre o rol...          │
├─────────────────────────────────────────┤
│  ● Ana García    Backend Eng   🟦  ⋮   │
│  ● Pedro Ruiz    Frontend Eng  🟧  ⋮   │
│  ...                                    │
├─────────────────────────────────────────┤
│  ▶ Archivados (2)                       │
└─────────────────────────────────────────┘
```

- **Dot de color**: círculo del color asignado al miembro
- **Menú ⋮**: "Renombrar", "Archivar", "Cambiar color"
- **Búsqueda**: filtra por `full_name` o `role` en tiempo real (sin backend call)
- **Sección archivados**: `ui.expansion` colapsado por defecto; tabla con columnas Nombre, Archivado el, botón "Reactivar"

### Modal "Añadir miembro"

Campos: Nombre completo (requerido), Rol (opcional).  
Botones: Cancelar / Guardar.  
Al guardar: llama `CreateMember`, refresca lista, muestra toast "Miembro creado".

### Modal "Renombrar"

Campos: Nombre completo (pre-relleno), Rol (pre-relleno).  
Llama `RenameMember`.

### Confirmación "Archivar"

`ui.notify` de confirmación o dialog simple: "¿Archivar a {nombre}? Sus datos se moverán a _archive/".  
Llama `ArchiveMember`. Si falla (error de filesystem), muestra error inline.

### Color picker

`ui.color_input` con paleta de 12 colores como sugerencias.  
Llama `UpdateMemberColor`.

## Página `/team/{slug}` — stub (`adapters/ui/pages/team_detail.py`)

Muestra nombre, rol y color del miembro. Label "Reuniones y reports — próximamente".  
Protegida con `@require_auth`.

## Registro en `app.py`

```python
from tla.adapters.ui.pages import team as _team_page          # noqa: F401
from tla.adapters.ui.pages import team_detail as _team_detail  # noqa: F401
```

## Enlace desde Inicio

La página `/` (index stub) añade un botón "Ver equipo →" que navega a `/team`.
