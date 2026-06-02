"""Use case: obtener un miembro por slug."""

from __future__ import annotations

from dataclasses import dataclass

from tla.domain.entities.member import TeamMember
from tla.domain.exceptions import MemberNotFoundError
from tla.domain.ports.member_repository import MemberRepository


@dataclass
class GetMember:
    repo: MemberRepository

    def execute(self, slug: str) -> TeamMember:
        member = self.repo.get(slug)
        if member is None:
            raise MemberNotFoundError(f"No existe el miembro '{slug}'.")
        return member
