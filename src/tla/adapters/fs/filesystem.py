"""Implementación real del FileSystemPort."""

from __future__ import annotations

import shutil
from pathlib import Path

from tla.adapters.fs.writer import atomic_write_text
from tla.domain.ports.filesystem import FileSystemPort


class LocalFileSystem(FileSystemPort):
    def exists(self, path: Path) -> bool:
        return path.exists()

    def mkdir(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def write_text(self, path: Path, content: str) -> None:
        atomic_write_text(path, content)

    def copy(self, src: Path, dst: Path) -> None:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def read_text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")
