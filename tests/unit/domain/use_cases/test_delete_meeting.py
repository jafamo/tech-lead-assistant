"""Tests unitarios: DeleteMeeting."""

from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tla.domain.entities.meeting import Meeting
from tla.domain.exceptions import MeetingNotFoundError
from tla.domain.use_cases.delete_meeting import DeleteMeeting


def _make_meeting() -> Meeting:
    return Meeting(
        id=1, team_member_id=1, team_member_slug="ana", meeting_type_id=1,
        meeting_type_slug="oneToOne", meeting_date=date(2024, 3, 15),
        title=None, transcript_path="ana/oneToOne/2024-03-15.transcript.txt",
        file_hash="abc", notes_path=None, is_shared=False,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_delete_success():
    repo, fs = MagicMock(), MagicMock()
    repo.get.return_value = _make_meeting()

    DeleteMeeting(repo=repo, fs=fs, data_root=Path("/data")).execute(1)

    fs.delete_transcript.assert_called_once_with(Path("/data"), "ana/oneToOne/2024-03-15.transcript.txt")
    repo.delete.assert_called_once_with(1)


def test_delete_not_found():
    repo = MagicMock()
    repo.get.return_value = None

    with pytest.raises(MeetingNotFoundError):
        DeleteMeeting(repo=repo, fs=MagicMock(), data_root=Path("/data")).execute(99)
