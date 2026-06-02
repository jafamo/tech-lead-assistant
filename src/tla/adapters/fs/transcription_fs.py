"""Implementación local del port TranscriptionFileSystemPort."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from tla.adapters.fs.writer import atomic_write_bytes, atomic_write_text
from tla.domain.ports.transcription_fs import TranscriptionFileSystemPort


class LocalTranscriptionFileSystem(TranscriptionFileSystemPort):
    def write_transcript(
        self,
        data_root: Path,
        slug: str,
        meeting_type_slug: str,
        meeting_date: date,
        ext: str,
        content: bytes,
    ) -> str:
        base = f"{meeting_date.isoformat()}.transcript{ext}"
        dest_dir = data_root / slug / meeting_type_slug
        dest = dest_dir / base
        # Sufijo si ya existe
        suffix = 2
        while dest.exists():
            dest = dest_dir / f"{meeting_date.isoformat()}_{suffix}.transcript{ext}"
            suffix += 1

        atomic_write_bytes(dest, content)
        return str(dest.relative_to(data_root))

    def read_transcript(self, data_root: Path, rel_path: str) -> str:
        return (data_root / rel_path).read_text(encoding="utf-8", errors="replace")

    def write_transcript_text(self, data_root: Path, rel_path: str, text: str) -> None:
        atomic_write_text(data_root / rel_path, text)

    def delete_transcript(self, data_root: Path, rel_path: str) -> None:
        path = data_root / rel_path
        path.unlink(missing_ok=True)
