"""Tests unitarios: RenameMember."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from tla.domain.entities.member import TeamMember
from tla.domain.exceptions import MemberNotFoundError
from tla.domain.use_cases.rename_member import RenameMember


def _make_member(slug="ana-garcia") -> TeamMember:
    return TeamMember(
        id=1, slug=slug, full_name="Ana García", role="Backend",
        color="#4A90D9", status="active", start_date=None,
        archived_at=None, created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_rename_success():
    repo = MagicMock()
    repo.get.return_value = _make_member()
    updated = _make_member()
    updated.full_name = "Ana García Pérez"
    repo.rename.return_value = updated

    result = RenameMember(repo=repo).execute("ana-garcia", "Ana García Pérez", "Senior Backend")

    repo.rename.assert_called_once_with("ana-garcia", "Ana García Pérez", "Senior Backend")
    assert result.full_name == "Ana García Pérez"


def test_rename_not_found():
    repo = MagicMock()
    repo.get.return_value = None

    with pytest.raises(MemberNotFoundError):
        RenameMember(repo=repo).execute("no-existe", "Nuevo Nombre")
