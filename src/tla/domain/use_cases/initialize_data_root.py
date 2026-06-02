"""Use case: inicializar la estructura de data_root."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tla.domain.ports.filesystem import FileSystemPort

_SUBDIRS = [
    "_import",
    "_stats/current/charts",
    "_stats/history",
    "_archive",
    "_shared/meetings",
    "_published_schema",
    "templates",
]


@dataclass
class InitializeDataRoot:
    fs: FileSystemPort

    def execute(self, data_root: Path) -> list[Path]:
        """Crea la estructura de data_root si no existe. Devuelve los dirs creados."""
        created: list[Path] = []

        if not self.fs.exists(data_root):
            self.fs.mkdir(data_root)
            created.append(data_root)

        for subdir in _SUBDIRS:
            path = data_root / subdir
            if not self.fs.exists(path):
                self.fs.mkdir(path)
                created.append(path)

        return created
