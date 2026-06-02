"""Use case: invalidar la sesión activa (logout / timeout)."""

from __future__ import annotations

from dataclasses import dataclass

from tla.domain.ports.session_store import SessionStore


@dataclass
class InvalidateSession:
    session_store: SessionStore

    def execute(self) -> None:
        self.session_store.invalidate()
