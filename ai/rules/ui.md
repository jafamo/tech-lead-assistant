# Reglas: UI (NiceGUI)

## Estructura
- Una página por fichero en `ui/pages/`.
- Componentes reutilizables en `ui/components/`.
- Layout compartido (sidebar, topbar) en `ui/layout/`.
- Las páginas llaman a servicios para la lógica; nunca implementan queries ni operaciones de filesystem.

## Diseño visual
- Interfaz amigable: iconos en todos los botones y acciones.
- Tooltips en botones de acción.
- Cada miembro tiene un color asignado — usarlo como acento visual (dot en tablas, barra en ficha, color en gráficos).
- Feedback visual obligatorio:
  - Operaciones >200ms → spinner.
  - Acciones exitosas → toast de confirmación.
  - Errores → popup con descripción y ruta del fichero si aplica.
  - Progreso de LLM → barra de progreso con opción de cancelar.
- Badges numéricos en sidebar para alertas (Inicio).

## Sidebar
- Items: 🏠 Inicio, 📄 Reports, 📊 Estadísticas, ⚙️ Settings.
- Colapsable (sólo iconos).
- Item activo resaltado.

## Tablas
- Todas las tablas con: búsqueda, filtros, ordenación.
- Botones de acción por fila con iconos.
- Indicadores de color del miembro como dot o barra.
- Fechas visibles y formateadas en hora local.

## Formularios
- Validación inline (no solo al submit).
- Campos requeridos marcados.
- Confirmación en acciones destructivas (archivar, sobrescribir, eliminar).

## Responsividad
- No mobile, pero sí adaptación a ventana redimensionada.
- Sidebar colapsable ayuda en ventanas estrechas.

## Modo oscuro/claro
- Toggle en Settings. NiceGUI lo soporta nativamente.
- Respectar `TLA_THEME` del `.env` como default.
