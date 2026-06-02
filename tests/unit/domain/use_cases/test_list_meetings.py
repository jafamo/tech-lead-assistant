"""Tests unitarios: ListMeetings."""

from datetime import date, datetime
from unittest.mock import MagicMock

from tla.domain.entities.meeting import Meeting
from tla.domain.use_cases.list_meetings import ListMeetings


def _make_meeting(mid: int = 1) -> Meeting:
    return Meeting(
        id=mid, team_member_id=1, team_member_slug="ana", meeting_type_id=1,
        meeting_type_slug="oneToOne", meeting_date=date(2024, 3, 15),
        title=None, transcript_path="ana/oneToOne/2024-03-15.transcript.txt",
        file_hash="abc", notes_path=None, is_shared=False,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_list_empty():
    repo = MagicMock()
    repo.list_for_member.return_value = []
    assert ListMeetings(repo=repo).execute(1) == []


def test_list_returns_results():
    repo = MagicMock()
    repo.list_for_member.return_value = [_make_meeting(1), _make_meeting(2)]
    result = ListMeetings(repo=repo).execute(1)
    assert len(result) == 2
    repo.list_for_member.assert_called_once_with(1)
