"""Use case: detectar si es el primer arranque."""

from __future__ import annotations

from dataclasses import dataclass

from tla.domain.ports.user_repository import UserRepository


@dataclass
class CheckFirstRun:
    repo: UserRepository

    def execute(self) -> bool:
        """Devuelve True si no existe ningún usuario (primer arranque)."""
        return not self.repo.exists()
