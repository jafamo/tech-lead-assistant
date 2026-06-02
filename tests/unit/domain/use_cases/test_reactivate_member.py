"""Tests unitarios: ReactivateMember."""

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tla.domain.entities.member import TeamMember
from tla.domain.exceptions import MemberNotArchivedError, MemberNotFoundError
from tla.domain.use_cases.reactivate_member import ReactivateMember


def _make_member(status="archived") -> TeamMember:
    return TeamMember(
        id=1, slug="ana-garcia", full_name="Ana García", role="Backend",
        color="#4A90D9", status=status, start_date=None,
        archived_at=None, created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_reactivate_success():
    repo = MagicMock()
    fs = MagicMock()
    repo.get.return_value = _make_member(status="archived")
    active = _make_member(status="active")
    repo.reactivate.return_value = active

    result = ReactivateMember(repo=repo, fs=fs, data_root=Path("/data")).execute("ana-garcia")

    fs.reactivate_member_dir.assert_called_once_with(Path("/data"), "ana-garcia")
    repo.reactivate.assert_called_once_with("ana-garcia")
    assert result.status == "active"


def test_reactivate_not_found():
    repo = MagicMock()
    repo.get.return_value = None

    with pytest.raises(MemberNotFoundError):
        ReactivateMember(repo=repo, fs=MagicMock(), data_root=Path("/data")).execute("no-existe")


def test_reactivate_not_archived():
    repo = MagicMock()
    repo.get.return_value = _make_member(status="active")

    with pytest.raises(MemberNotArchivedError):
        ReactivateMember(repo=repo, fs=MagicMock(), data_root=Path("/data")).execute("ana-garcia")
