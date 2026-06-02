"""Tests unitarios: UpdateMemberColor."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from tla.domain.entities.member import TeamMember
from tla.domain.exceptions import InvalidColorError, MemberNotFoundError
from tla.domain.use_cases.update_member_color import UpdateMemberColor


def _make_member() -> TeamMember:
    return TeamMember(
        id=1, slug="ana-garcia", full_name="Ana García", role=None,
        color="#4A90D9", status="active", start_date=None,
        archived_at=None, created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_update_color_success():
    repo = MagicMock()
    repo.get.return_value = _make_member()
    updated = _make_member()
    updated.color = "#E67E22"
    repo.update_color.return_value = updated

    result = UpdateMemberColor(repo=repo).execute("ana-garcia", "#E67E22")

    repo.update_color.assert_called_once_with("ana-garcia", "#E67E22")
    assert result.color == "#E67E22"


def test_update_color_invalid_format():
    repo = MagicMock()

    with pytest.raises(InvalidColorError):
        UpdateMemberColor(repo=repo).execute("ana-garcia", "rojo")


def test_update_color_not_found():
    repo = MagicMock()
    repo.get.return_value = None

    with pytest.raises(MemberNotFoundError):
        UpdateMemberColor(repo=repo).execute("no-existe", "#4A90D9")
