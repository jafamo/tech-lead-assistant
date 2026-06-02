## Why

TLA maneja datos personales y sensibles de los miembros del equipo. Sin autenticación, cualquiera con acceso físico al equipo puede abrir la app y leer toda esa información. El lock-screen es la barrera mínima necesaria antes de poder usar cualquier otra funcionalidad.

## What Changes

- Nueva pantalla de **primer arranque** (wizard): crear username + password, confirmar `TLA_DATA_ROOT`.
- Nueva pantalla de **lock-screen**: campo de password, botón desbloquear, retardo exponencial tras fallos.
- **Timeout de sesión** por inactividad configurable (`TLA_SESSION_TIMEOUT_MIN`).
- **Cambio de password** desde Settings (requiere password actual).
- Routing de arranque: si no hay cuenta → wizard; si hay cuenta → lock-screen; si está autenticado → Inicio.
- Banner de recomendación de Full Disk Encryption en el primer arranque.

## Capabilities

### New Capabilities

- `user-auth`: gestión de credenciales (crear usuario, verificar password con bcrypt, retardo exponencial)
- `session-management`: ciclo de vida de la sesión (login, logout, timeout por inactividad)
- `first-run-wizard`: flujo de primer arranque (crear cuenta + confirmar data_root + banner FDE)
- `lock-screen-ui`: interfaz de lock-screen y enrutamiento de arranque

### Modified Capabilities

## Impact

- `src/tla/app.py`: añadir routing de arranque (wizard / lock-screen / home)
- `src/tla/auth.py`: nuevo módulo con lógica de autenticación
- `src/tla/adapters/db/models.py`: ya existe la tabla `User` (creada en 001-bootstrap)
- Nueva dependencia: `bcrypt>=4.0` (ya en `pyproject.toml`)
- Nueva dependencia UI: páginas `login.py` y `first_run.py` en `adapters/ui/pages/`
