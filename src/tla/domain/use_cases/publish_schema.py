"""Use case: publicar content.schema.json en data_root/_published_schema/."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tla.domain.ports.filesystem import FileSystemPort


@dataclass
class PublishSchema:
    fs: FileSystemPort

    def execute(self, schema_src: Path, data_root: Path) -> Path:
        """Copia schema_src a data_root/_published_schema/content.schema.json."""
        dst = data_root / "_published_schema" / "content.schema.json"
        self.fs.mkdir(dst.parent)
        self.fs.copy(schema_src, dst)
        return dst
