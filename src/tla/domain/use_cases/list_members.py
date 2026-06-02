"""Use case: listar miembros del equipo."""

from __future__ import annotations

from dataclasses import dataclass

from tla.domain.entities.member import TeamMember
from tla.domain.ports.member_repository import MemberRepository


@dataclass
class ListMembers:
    repo: MemberRepository

    def execute(self, include_archived: bool = False) -> list[TeamMember]:
        if include_archived:
            return self.repo.list_all()
        return self.repo.list_active()
