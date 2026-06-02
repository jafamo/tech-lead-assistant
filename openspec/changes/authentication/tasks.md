## 1. Domain — Entidades y ports

- [x] 1.1 Entidad `AuthSession` (dataclass: `user_id`, `started_at`, `last_activity_at`)
- [x] 1.2 Port `UserRepository` (ABC: `create`, `get`, `exists`, `update_password`)
- [x] 1.3 Port `SessionStore` (ABC: `create_session`, `get_session`, `invalidate`, `update_activity`)

## 2. Domain — Use cases

- [x] 2.1 Use case `CreateUser` — crea cuenta, valida unicidad y longitud de password mínima (8 chars), hashea con bcrypt cost ≥ 12
- [x] 2.2 Use case `Authenticate` — verifica password, retardo exponencial tras ≥ 3 fallos, resetea contador en éxito
- [x] 2.3 Use case `ChangePassword` — requiere password actual correcto, re-hashea nuevo password
- [x] 2.4 Use case `CheckFirstRun` — devuelve `True` si no existe ningún usuario en BD
- [x] 2.5 Use case `InvalidateSession` — limpia la sesión activa (logout y timeout)

## 3. Domain — Tests unitarios

- [x] 3.1 Test `CreateUser`: éxito, cuenta duplicada rechazada, password corto rechazado
- [x] 3.2 Test `Authenticate`: password correcto, password incorrecto, retardo exponencial, reseteo de contador
- [x] 3.3 Test `ChangePassword`: éxito, password actual incorrecto
- [x] 3.4 Test `CheckFirstRun`: sin usuario → True, con usuario → False
- [x] 3.5 Test `InvalidateSession`: sesión limpiada

## 4. Adapters — DB y sesión

- [x] 4.1 `adapters/db/user_repo.py` — implementa `UserRepository` con SQLModel
- [x] 4.2 `auth.py` — módulo de sesión en memoria: `InMemorySessionStore` implementa `SessionStore`, timer de inactividad con `asyncio`

## 5. Adapters — Tests de integración

- [x] 5.1 Test integración `UserRepository` contra SQLite en memoria: crear, obtener, exists, update_password

## 6. UI — Lock-screen

- [x] 6.1 `adapters/ui/pages/login.py` — página `/login`: campo password, botón desbloquear, mensaje de error inline
- [x] 6.2 Deshabilitar input + mostrar countdown durante backoff exponencial

## 7. UI — Wizard de primer arranque

- [x] 7.1 `adapters/ui/pages/first_run.py` — página `/first-run` con dos pasos:
  - Paso 1: username + password + confirmación
  - Paso 2: confirmar / cambiar `TLA_DATA_ROOT` con folder picker
- [x] 7.2 Banner FDE tras completar wizard (BitLocker / LUKS / FileVault según SO)
- [x] 7.3 Llamar a `InitializeDataRoot` y `PublishSchema` al completar wizard

## 8. Routing de arranque

- [x] 8.1 Actualizar `app.py`: routing en `/` según estado (wizard / lock-screen / home)
- [x] 8.2 Decorator `@require_auth` — redirige a `/login` si no hay sesión activa
- [x] 8.3 Aplicar `@require_auth` a la ruta `/` (Inicio)

## 9. Settings — Cambio de password

- [x] 9.1 Añadir sección "Cambiar password" en `adapters/ui/pages/settings.py` (stub de página si no existe aún)
- [x] 9.2 Modal con campo "password actual" + "nuevo password" + confirmación
