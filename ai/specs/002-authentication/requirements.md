# 002 — Autenticación (Lock-Screen)

**Prioridad**: 2 (necesario antes de cualquier pantalla de la app)
**Rama**: `feature/002-authentication`
**Depende de**: 001-bootstrap

## Descripción

Sistema de autenticación como lock-screen local. No cifra los datos — la seguridad de los ficheros se delega al FDE del SO.

## Requisitos funcionales

Extraídos de §6.1 de la spec:

- **RF-AUTH-1**: Primer arranque → wizard para crear username + password (ver 001-bootstrap). Si ya existe cuenta → ir a lock-screen directamente.
- **RF-AUTH-2**: Lock-screen en arranques posteriores: campo de password, botón de desbloquear.
- **RF-AUTH-3**: Password hasheado con bcrypt (cost factor ≥ 12). Nunca en claro ni en logs.
- **RF-AUTH-4**: Retardo exponencial tras 3 intentos fallidos (1 s, 2 s, 4 s…). Sin bloqueo permanente.
- **RF-AUTH-5**: Timeout de inactividad configurable (`TLA_SESSION_TIMEOUT_MIN`, default 30 min). Al expirar → volver al lock-screen.
- **RF-AUTH-6**: Cambio de password desde Settings (requiere password actual).

## Casos de uso relacionados

- UC1–UC12 todos: el usuario debe estar autenticado para cualquier operación.

## Requisitos no funcionales

- Password nunca sale de la capa de autenticación (`auth.py`). No se logea.
- El lock-screen es la única pantalla accesible sin autenticación.
- Usar tabla `user` del índice SQLite (siempre local).
