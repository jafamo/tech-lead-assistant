"""Port: repositorio de usuarios."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from tla.adapters.db.models import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, username: str, password_hash: str) -> User: ...

    @abstractmethod
    def get(self) -> Optional[User]:
        """Devuelve el único usuario de la app, o None si no existe."""

    @abstractmethod
    def exists(self) -> bool:
        """True si hay al menos un usuario registrado."""

    @abstractmethod
    def update_password(self, user_id: int, new_hash: str) -> None: ...
