"""Tests unitarios: ArchiveMember."""

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tla.domain.entities.member import TeamMember
from tla.domain.exceptions import MemberAlreadyArchivedError, MemberNotFoundError
from tla.domain.use_cases.archive_member import ArchiveMember


def _make_member(status="active") -> TeamMember:
    return TeamMember(
        id=1, slug="ana-garcia", full_name="Ana García", role="Backend",
        color="#4A90D9", status=status, start_date=None,
        archived_at=None, created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_archive_success():
    repo = MagicMock()
    fs = MagicMock()
    repo.get.return_value = _make_member(status="active")
    archived = _make_member(status="archived")
    repo.archive.return_value = archived

    result = ArchiveMember(repo=repo, fs=fs, data_root=Path("/data")).execute("ana-garcia")

    fs.archive_member_dir.assert_called_once_with(Path("/data"), "ana-garcia")
    repo.archive.assert_called_once_with("ana-garcia")
    assert result.status == "archived"


def test_archive_not_found():
    repo = MagicMock()
    repo.get.return_value = None

    with pytest.raises(MemberNotFoundError):
        ArchiveMember(repo=repo, fs=MagicMock(), data_root=Path("/data")).execute("no-existe")


def test_archive_already_archived():
    repo = MagicMock()
    repo.get.return_value = _make_member(status="archived")

    with pytest.raises(MemberAlreadyArchivedError):
        ArchiveMember(repo=repo, fs=MagicMock(), data_root=Path("/data")).execute("ana-garcia")
