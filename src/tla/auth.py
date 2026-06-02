"""Gestión de sesión en memoria e InMemorySessionStore."""

from __future__ import annotations

from typing import Optional

from tla.domain.entities.auth import AuthSession
from tla.domain.ports.session_store import SessionStore

# Sesión global única (single-user, en memoria, no persiste entre reinicios)
_session: Optional[AuthSession] = None


class InMemorySessionStore(SessionStore):
    def create_session(self, user_id: int) -> AuthSession:
        global _session
        _session = AuthSession(user_id=user_id)
        return _session

    def get_session(self) -> Optional[AuthSession]:
        return _session

    def invalidate(self) -> None:
        global _session
        _session = None

    def update_activity(self) -> None:
        if _session is not None:
            _session.touch()


def is_authenticated() -> bool:
    return _session is not None


def get_current_session() -> Optional[AuthSession]:
    return _session
