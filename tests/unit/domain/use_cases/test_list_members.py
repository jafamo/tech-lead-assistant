"""Tests unitarios: ListMembers."""

from datetime import datetime
from unittest.mock import MagicMock

from tla.domain.entities.member import TeamMember
from tla.domain.use_cases.list_members import ListMembers


def _member(slug: str, status: str = "active") -> TeamMember:
    return TeamMember(
        id=1, slug=slug, full_name=slug, role=None,
        color="#4A90D9", status=status, start_date=None,
        archived_at=None, created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_list_active_only():
    repo = MagicMock()
    repo.list_active.return_value = [_member("ana")]

    result = ListMembers(repo=repo).execute(include_archived=False)

    repo.list_active.assert_called_once()
    repo.list_all.assert_not_called()
    assert len(result) == 1


def test_list_all():
    repo = MagicMock()
    repo.list_all.return_value = [_member("ana"), _member("pedro", "archived")]

    result = ListMembers(repo=repo).execute(include_archived=True)

    repo.list_all.assert_called_once()
    assert len(result) == 2
