"""Use case: obtener una reunión por id."""

from __future__ import annotations

from dataclasses import dataclass

from tla.domain.entities.meeting import Meeting
from tla.domain.exceptions import MeetingNotFoundError
from tla.domain.ports.meeting_repository import MeetingRepository


@dataclass
class GetMeeting:
    repo: MeetingRepository

    def execute(self, meeting_id: int) -> Meeting:
        meeting = self.repo.get(meeting_id)
        if meeting is None:
            raise MeetingNotFoundError(f"No existe la reunión con id {meeting_id}.")
        return meeting
