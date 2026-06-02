"""Use case: crear un nuevo miembro del equipo."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from tla.domain.entities.member import MEMBER_COLOR_PALETTE, TeamMember
from tla.domain.ports.member_fs import MemberFileSystemPort
from tla.domain.ports.member_repository import MemberRepository


def _slugify(text: str) -> str:
    text = text.lower().strip()
    # Transliterate common accented chars
    replacements = str.maketrans("áéíóúüñàèìòùâêîôûäëïöü", "aeiouunaeiouaeiouaeiou")
    text = text.translate(replacements)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


@dataclass
class CreateMember:
    repo: MemberRepository
    fs: MemberFileSystemPort
    data_root: Path

    def execute(self, full_name: str, role: Optional[str] = None) -> TeamMember:
        base_slug = _slugify(full_name)
        slug = base_slug
        suffix = 2
        while self.repo.get(slug) is not None:
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        color = MEMBER_COLOR_PALETTE[self.repo.count_active() % len(MEMBER_COLOR_PALETTE)]
        member = self.repo.create(slug=slug, full_name=full_name, role=role, color=color)
        self.fs.initialize_member_dir(self.data_root, slug, full_name, role)
        return member
