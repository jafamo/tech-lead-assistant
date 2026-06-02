"""Use case: búsqueda full-text de reuniones."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from tla.domain.entities.meeting import Meeting
from tla.domain.ports.meeting_repository import MeetingRepository


@dataclass
class SearchMeetings:
    repo: MeetingRepository

    def execute(self, query: str, member_slug: Optional[str] = None) -> list[Meeting]:
        if not query.strip():
            return []
        return self.repo.search_fts(query.strip(), member_slug)
