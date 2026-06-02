# 002 — Autenticación: Tasks

**Estado**: ⬜ Pendiente

## Domain

- [ ] Entidad `User` (username, password_hash)
- [ ] Use case `CreateUser` — primer arranque
- [ ] Use case `Authenticate` — verifica password (bcrypt), gestiona retardo exponencial
- [ ] Use case `ChangePassword` — requiere password actual
- [ ] Use case `CheckSessionTimeout` — detecta inactividad
- [ ] Port `UserRepository` — interfaz CRUD de usuario
- [ ] Tests unitarios de todos los use cases (port mockeado)

## Adapters

- [ ] `adapters/db/user_repo.py` — implementa `UserRepository` con SQLModel
- [ ] `auth.py` — bcrypt hash/verify, lógica de retardo exponencial, gestión de sesión

## UI

- [ ] `adapters/ui/pages/login.py` — lock-screen: campo password + botón desbloquear
- [ ] Retardo visual tras intentos fallidos (contador)
- [ ] Timeout de inactividad → volver a lock-screen automáticamente
- [ ] Cambio de password en Settings (ver 010-settings)

## Tests

- [ ] Test unitario: `CreateUser` — hash correcto, no guarda en claro
- [ ] Test unitario: `Authenticate` — ok, fallo, retardo exponencial
- [ ] Test unitario: `ChangePassword` — requiere password actual
- [ ] Test integración: `UserRepository` contra SQLite en memoria
