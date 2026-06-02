"""Port: operaciones de filesystem para miembros del equipo."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class MemberFileSystemPort(ABC):
    @abstractmethod
    def initialize_member_dir(
        self, data_root: Path, slug: str, full_name: str, role: Optional[str]
    ) -> None: ...

    @abstractmethod
    def archive_member_dir(self, data_root: Path, slug: str) -> None: ...

    @abstractmethod
    def reactivate_member_dir(self, data_root: Path, slug: str) -> None: ...

    @abstractmethod
    def member_dir_exists(self, data_root: Path, slug: str) -> bool: ...
