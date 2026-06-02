"""Tests unitarios: SearchMeetings."""

from datetime import date, datetime
from unittest.mock import MagicMock

from tla.domain.entities.meeting import Meeting
from tla.domain.use_cases.search_meetings import SearchMeetings


def _make_meeting() -> Meeting:
    return Meeting(
        id=1, team_member_id=1, team_member_slug="ana", meeting_type_id=1,
        meeting_type_slug="oneToOne", meeting_date=date(2024, 3, 15),
        title=None, transcript_path="ana/oneToOne/2024-03-15.transcript.txt",
        file_hash="abc", notes_path=None, is_shared=False,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_search_returns_results():
    repo = MagicMock()
    repo.search_fts.return_value = [_make_meeting()]
    result = SearchMeetings(repo=repo).execute("feedback")
    assert len(result) == 1
    repo.search_fts.assert_called_once_with("feedback", None)


def test_search_empty_query_returns_nothing():
    repo = MagicMock()
    result = SearchMeetings(repo=repo).execute("   ")
    assert result == []
    repo.search_fts.assert_not_called()


def test_search_with_member_filter():
    repo = MagicMock()
    repo.search_fts.return_value = []
    SearchMeetings(repo=repo).execute("reunión", member_slug="ana")
    repo.search_fts.assert_called_once_with("reunión", "ana")
