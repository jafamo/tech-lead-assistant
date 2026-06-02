"""Port: operaciones de filesystem (abstracción para tests)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class FileSystemPort(ABC):
    @abstractmethod
    def exists(self, path: Path) -> bool: ...

    @abstractmethod
    def mkdir(self, path: Path) -> None:
        """Crea el directorio y los padres si no existen."""

    @abstractmethod
    def write_text(self, path: Path, content: str) -> None:
        """Escritura atómica de texto."""

    @abstractmethod
    def copy(self, src: Path, dst: Path) -> None:
        """Copia src a dst de forma atómica."""

    @abstractmethod
    def read_text(self, path: Path) -> str: ...
