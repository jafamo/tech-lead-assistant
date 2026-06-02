"""Port: operaciones de filesystem para transcripciones."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path


class TranscriptionFileSystemPort(ABC):
    @abstractmethod
    def write_transcript(
        self,
        data_root: Path,
        slug: str,
        meeting_type_slug: str,
        meeting_date: date,
        ext: str,
        content: bytes,
    ) -> str:
        """Escribe la transcripción y devuelve la ruta relativa a data_root."""
        ...

    @abstractmethod
    def read_transcript(self, data_root: Path, rel_path: str) -> str: ...

    @abstractmethod
    def write_transcript_text(self, data_root: Path, rel_path: str, text: str) -> None:
        """Reescritura atómica (para edición)."""
        ...

    @abstractmethod
    def delete_transcript(self, data_root: Path, rel_path: str) -> None: ...
