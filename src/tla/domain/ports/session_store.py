"""Port: almacén de sesión activa."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from tla.domain.entities.auth import AuthSession


class SessionStore(ABC):
    @abstractmethod
    def create_session(self, user_id: int) -> AuthSession: ...

    @abstractmethod
    def get_session(self) -> Optional[AuthSession]: ...

    @abstractmethod
    def invalidate(self) -> None: ...

    @abstractmethod
    def update_activity(self) -> None:
        """Actualiza last_activity_at de la sesión activa."""
