# 007 — Inicio, Navegación y Banner de Alertas

**Prioridad**: 7 (shell de la UI — integra todo lo anterior)
**Rama**: `feature/007-home-navigation`
**Depende de**: 002-authentication, 003-team-management, 005-report-generation

## Descripción

Sidebar de navegación persistente, página de Inicio con tabla del personal y banner de alertas/pendientes.

## Requisitos funcionales

### Sidebar (§6.11)
- **RF-NAV-1**: Sidebar persistente con items:
  1. 🏠 **Inicio** — activo por defecto tras login. Badge rojo con número total de alertas.
  2. 📄 **Reports**
  3. 📊 **Estadísticas**
  4. ⚙️ **Settings** (al final, separado visualmente)
- **RF-NAV-2**: Sección activa resaltada con color de acento.
- **RF-NAV-3**: Sidebar colapsable (solo iconos cuando colapsado).
- **RF-NAV-4**: Icono + texto en cada item.

### Página Inicio (§6.12)
- **RF-HOME-1**: Vista por defecto tras login.
- **RF-HOME-2**: Banner de alertas/pendientes (ver abajo).
- **RF-HOME-3**: Tabla del personal con columnas:
  - 🎨 Dot de color del miembro
  - Nombre (clickeable → vista de detalle)
  - Rol
  - Última reunión (fecha; en rojo si > 3 semanas)
  - Próxima reunión programada (fecha en verde si futura, rojo si vencida)
  - Action items abiertos (badge con count; naranja si > 0, rojo si alguno > 30 días)
  - Último report (periodo + modo con icono + fecha)
  - Acciones (botones con iconos por fila):
    - 📝 **Generar report** → modal LLM + periodo
    - 📥 **Importar report** → importar desde staging dir
    - 👁️ **Ver último report** → navega al report más reciente
    - 📤 **Exportar** → diálogo export (PDF/MD/CSV)
- **RF-HOME-4**: Buscador rápido sobre la tabla (por nombre o rol).
- **RF-HOME-5**: Link "👥 Ver archivados (N)" bajo la tabla si hay miembros archivados.

### Banner de alertas/pendientes (§6.10)
- **RF-BANNER-1**: Banda visible en la parte superior de Inicio. Icono + texto por alerta.
- **RF-BANNER-2**: Tipos de alertas:
  - 🗓️ Reuniones programadas esta semana
  - ⚠️ Reuniones vencidas (pasadas y no marcadas como completadas/canceladas)
  - 📋 Action items abiertos > 30 días (por miembro, con color)
  - 🔄 Temas recurrentes detectados en ≥ 3 reports recientes
  - 👤 Miembros sin reunión registrada en > 3 semanas
  - 📥 Reports disponibles en staging dir pendientes de importar
  - 🔌 `data_root` desconectado (si está en red)
- **RF-BANNER-3**: Cada alerta es clickeable → navega a la reunión, miembro o report relevante.
- **RF-BANNER-4**: El count total de alertas aparece en el sidebar junto a "Inicio" como badge.

## Casos de uso relacionados

- UC7: Ver banner de reuniones pendientes esta semana.
- UC10: Desde Inicio, ver tabla del personal y generar/importar/ver/exportar report.

## Diseño visual

Ver wireframe en Excalidraw: https://excalidraw.com/#json=n2_VD9tujCCtWlYKHEicQ,OoaOtIwA2DJBffv82PwjqQ
