"""Use case: cambiar el color asignado a un miembro."""

from __future__ import annotations

import re
from dataclasses import dataclass

from tla.domain.entities.member import TeamMember
from tla.domain.exceptions import InvalidColorError, MemberNotFoundError
from tla.domain.ports.member_repository import MemberRepository

_HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


@dataclass
class UpdateMemberColor:
    repo: MemberRepository

    def execute(self, slug: str, color: str) -> TeamMember:
        if not _HEX_COLOR_RE.match(color):
            raise InvalidColorError(f"Color inválido: '{color}'. Formato esperado: #RRGGBB.")
        if self.repo.get(slug) is None:
            raise MemberNotFoundError(f"No existe el miembro '{slug}'.")
        return self.repo.update_color(slug, color)
