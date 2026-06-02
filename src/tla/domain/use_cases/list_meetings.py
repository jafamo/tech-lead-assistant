"""Use case: listar reuniones de un miembro."""

from __future__ import annotations

from dataclasses import dataclass

from tla.domain.entities.meeting import Meeting
from tla.domain.ports.meeting_repository import MeetingRepository


@dataclass
class ListMeetings:
    repo: MeetingRepository

    def execute(self, team_member_id: int) -> list[Meeting]:
        return self.repo.list_for_member(team_member_id)
