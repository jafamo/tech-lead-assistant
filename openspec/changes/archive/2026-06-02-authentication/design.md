## Context

La infraestructura del 001-bootstrap ya creó la tabla `User` en SQLite y el módulo `config.py` con `TLA_SESSION_TIMEOUT_MIN`. La app arranca con NiceGUI sobre un servidor local (`http://127.0.0.1:8080`). No hay estado de sesión persistente entre reinicios — el login es siempre obligatorio al arrancar.

## Goals / Non-Goals

**Goals:**
- Lock-screen funcional antes de exponer cualquier dato del equipo.
- Wizard de primer arranque que inicializa cuenta + data_root en una sola pasada.
- Timeout de inactividad que vuelve al lock-screen automáticamente.
- Cambio de password seguro desde Settings.

**Non-Goals:**
- Multi-usuario (v1 es single-user).
- Recuperación de password olvidado (app local, sin email).
- Cifrado de ficheros (delegado a FDE del SO).
- 2FA o SSO.

## Decisions

### D1: bcrypt para hashing, cost factor ≥ 12
bcrypt sobre argon2 o scrypt por madurez y soporte nativo en Python (`bcrypt` library). Cost 12 es el mínimo razonable para 2025 en hardware moderno. El hash se almacena en la tabla `User` — la única tabla que vive en `TLA_DB_PATH` (siempre local).

### D2: Estado de sesión en memoria, no en disco
La sesión se guarda como variable de módulo en `auth.py` (`_session: AuthSession | None`). No persiste entre reinicios — al arrancar siempre hay que hacer login. Esto evita tokens robados de disco y simplifica el modelo.

### D3: Retardo exponencial client-side en NiceGUI
Tras 3 intentos fallidos: 1 s, 2 s, 4 s… implementado con `asyncio.sleep` en el handler del formulario. No bloqueo permanente — el retardo máximo es 32 s (6 intentos), suficiente para desincentivar fuerza bruta sin romper UX.

### D4: Routing en `app.py` basado en estado de sesión
`app.py` registra tres rutas NiceGUI:
- `/` → redirige según estado (wizard / lock / home)
- `/first-run` → wizard (solo accesible si no hay usuario en BD)
- `/login` → lock-screen

El guard se implementa como decorator `@require_auth` que redirige a `/login` si no hay sesión activa.

### D5: Timeout con `ui.timer` de NiceGUI
Un timer de 60 s comprueba el timestamp de última actividad. Si supera `TLA_SESSION_TIMEOUT_MIN`, invalida la sesión y redirige al lock-screen. La actividad se actualiza en cada petición HTTP vía middleware.

## Risks / Trade-offs

- **[Risk] Single-user hardcoded** → Si en el futuro se necesita multi-usuario, `auth.py` tendrá que refactorizarse para soportar múltiples sesiones. Mitigación: mantener `UserRepository` como port para facilitar el cambio.
- **[Risk] NiceGUI sin middleware HTTP estándar** → El tracking de actividad se hace a nivel de componente (eventos de UI), no de petición HTTP. Mitigación: actualizar timestamp en cada interacción de usuario con un handler global.
- **[Risk] DB siempre local pero app puede estar en red** → Si el usuario mueve `TLA_DB_PATH` a red, el hash queda expuesto. Mitigación: validar en arranque que `TLA_DB_PATH` es local y advertir si no lo es.
