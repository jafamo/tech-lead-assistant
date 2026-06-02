"""Use case: renombrar miembro (slug inmutable)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from tla.domain.entities.member import TeamMember
from tla.domain.exceptions import MemberNotFoundError
from tla.domain.ports.member_repository import MemberRepository


@dataclass
class RenameMember:
    repo: MemberRepository

    def execute(self, slug: str, new_full_name: str, new_role: Optional[str] = None) -> TeamMember:
        if self.repo.get(slug) is None:
            raise MemberNotFoundError(f"No existe el miembro '{slug}'.")
        return self.repo.rename(slug, new_full_name, new_role)
