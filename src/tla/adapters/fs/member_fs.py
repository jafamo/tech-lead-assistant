"""Implementación local del port MemberFileSystemPort."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader

from tla.adapters.fs.writer import atomic_write_text
from tla.domain.exceptions import AtomicWriteError
from tla.domain.ports.member_fs import MemberFileSystemPort

_MEMBER_SUBDIRS = [
    "profile",
    "oneToOne",
    "seguimiento",
    "feedback",
    "tecnica",
    "retro",
    "notes",
    "reports",
]

_TEMPLATES_DIR = Path(__file__).parents[2] / "templates"


class LocalMemberFileSystem(MemberFileSystemPort):
    def initialize_member_dir(
        self, data_root: Path, slug: str, full_name: str, role: Optional[str]
    ) -> None:
        member_dir = data_root / slug
        for subdir in _MEMBER_SUBDIRS:
            (member_dir / subdir).mkdir(parents=True, exist_ok=True)

        env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), autoescape=False)
        template = env.get_template("profile.md.j2")
        content = template.render(full_name=full_name, role=role, slug=slug, start_date=None)
        atomic_write_text(member_dir / "profile" / "profile.md", content)

    def archive_member_dir(self, data_root: Path, slug: str) -> None:
        src = data_root / slug
        dst = data_root / "_archive" / slug
        if dst.exists():
            raise AtomicWriteError(f"Ya existe '{dst}' en _archive/.")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

    def reactivate_member_dir(self, data_root: Path, slug: str) -> None:
        src = data_root / "_archive" / slug
        dst = data_root / slug
        if dst.exists():
            raise AtomicWriteError(f"Ya existe '{dst}' en data_root/.")
        shutil.move(str(src), str(dst))

    def member_dir_exists(self, data_root: Path, slug: str) -> bool:
        return (data_root / slug).exists()
