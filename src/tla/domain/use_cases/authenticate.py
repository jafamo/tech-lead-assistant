"""Use case: autenticar al usuario con retardo exponencial."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

import bcrypt

from tla.domain.entities.auth import AuthSession
from tla.domain.exceptions import TLAError
from tla.domain.ports.session_store import SessionStore
from tla.domain.ports.user_repository import UserRepository

_BACKOFF_THRESHOLD = 3
_BACKOFF_MAX_SECONDS = 32


class AuthenticationError(TLAError):
    pass


class NoUserError(TLAError):
    pass


@dataclass
class Authenticate:
    repo: UserRepository
    session_store: SessionStore
    _failed_attempts: int = field(default=0, init=False)

    async def execute(self, password: str) -> AuthSession:
        user = self.repo.get()
        if user is None:
            raise NoUserError("No hay ningún usuario registrado.")

        await self._apply_backoff()

        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            self._failed_attempts += 1
            raise AuthenticationError("Contraseña incorrecta.")

        self._failed_attempts = 0
        return self.session_store.create_session(user_id=user.id)  # type: ignore[arg-type]

    async def _apply_backoff(self) -> None:
        if self._failed_attempts >= _BACKOFF_THRESHOLD:
            delay = min(2 ** (self._failed_attempts - _BACKOFF_THRESHOLD), _BACKOFF_MAX_SECONDS)
            await asyncio.sleep(delay)

    @property
    def failed_attempts(self) -> int:
        return self._failed_attempts

    @property
    def backoff_seconds(self) -> int:
        if self._failed_attempts < _BACKOFF_THRESHOLD:
            return 0
        return min(2 ** (self._failed_attempts - _BACKOFF_THRESHOLD), _BACKOFF_MAX_SECONDS)
