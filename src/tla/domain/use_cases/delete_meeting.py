"""Use case: eliminar una transcripción."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tla.domain.exceptions import MeetingNotFoundError
from tla.domain.ports.meeting_repository import MeetingRepository
from tla.domain.ports.transcription_fs import TranscriptionFileSystemPort


@dataclass
class DeleteMeeting:
    repo: MeetingRepository
    fs: TranscriptionFileSystemPort
    data_root: Path

    def execute(self, meeting_id: int) -> None:
        meeting = self.repo.get(meeting_id)
        if meeting is None:
            raise MeetingNotFoundError(f"No existe la reunión con id {meeting_id}.")
        self.fs.delete_transcript(self.data_root, meeting.transcript_path)
        self.repo.delete(meeting_id)
