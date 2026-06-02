"""Use case: reactivar miembro archivado."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tla.domain.entities.member import TeamMember
from tla.domain.exceptions import MemberNotArchivedError, MemberNotFoundError
from tla.domain.ports.member_fs import MemberFileSystemPort
from tla.domain.ports.member_repository import MemberRepository


@dataclass
class ReactivateMember:
    repo: MemberRepository
    fs: MemberFileSystemPort
    data_root: Path

    def execute(self, slug: str) -> TeamMember:
        member = self.repo.get(slug)
        if member is None:
            raise MemberNotFoundError(f"No existe el miembro '{slug}'.")
        if member.status != "archived":
            raise MemberNotArchivedError(f"El miembro '{slug}' no está archivado.")
        self.fs.reactivate_member_dir(self.data_root, slug)
        return self.repo.reactivate(slug)
