"""Port: repositorio de miembros del equipo."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from tla.domain.entities.member import TeamMember


class MemberRepository(ABC):
    @abstractmethod
    def create(self, slug: str, full_name: str, role: Optional[str], color: str) -> TeamMember: ...

    @abstractmethod
    def get(self, slug: str) -> Optional[TeamMember]: ...

    @abstractmethod
    def list_active(self) -> list[TeamMember]: ...

    @abstractmethod
    def list_all(self) -> list[TeamMember]: ...

    @abstractmethod
    def count_active(self) -> int: ...

    @abstractmethod
    def rename(self, slug: str, new_full_name: str, new_role: Optional[str]) -> TeamMember: ...

    @abstractmethod
    def archive(self, slug: str) -> TeamMember: ...

    @abstractmethod
    def reactivate(self, slug: str) -> TeamMember: ...

    @abstractmethod
    def update_color(self, slug: str, color: str) -> TeamMember: ...
