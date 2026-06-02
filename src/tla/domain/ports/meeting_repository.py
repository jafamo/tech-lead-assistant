"""Port: repositorio de reuniones."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from tla.domain.entities.meeting import Meeting


class MeetingRepository(ABC):
    @abstractmethod
    def create(
        self,
        team_member_id: int,
        meeting_type_id: int,
        meeting_date: date,
        transcript_path: str,
        file_hash: str,
        title: Optional[str] = None,
    ) -> Meeting: ...

    @abstractmethod
    def get(self, meeting_id: int) -> Optional[Meeting]: ...

    @abstractmethod
    def list_for_member(self, team_member_id: int) -> list[Meeting]: ...

    @abstractmethod
    def hash_exists(self, file_hash: str) -> bool: ...

    @abstractmethod
    def delete(self, meeting_id: int) -> None: ...

    @abstractmethod
    def index_fts(
        self, meeting_id: int, content: str, member_slug: str, doc_type: str
    ) -> None: ...

    @abstractmethod
    def search_fts(
        self, query: str, member_slug: Optional[str] = None
    ) -> list[Meeting]: ...
