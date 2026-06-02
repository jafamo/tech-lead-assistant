"""Tests unitarios: CreateMember."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tla.domain.entities.member import MEMBER_COLOR_PALETTE, TeamMember
from tla.domain.use_cases.create_member import CreateMember, _slugify


def _make_member(slug="ana-garcia", color="#4A90D9") -> TeamMember:
    from datetime import datetime
    return TeamMember(
        id=1, slug=slug, full_name="Ana García", role="Backend",
        color=color, status="active", start_date=None,
        archived_at=None, created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def test_slugify_basic():
    assert _slugify("Ana García") == "ana-garcia"


def test_slugify_special_chars():
    assert _slugify("José López") == "jose-lopez"


def test_create_success():
    repo = MagicMock()
    fs = MagicMock()
    repo.get.return_value = None
    repo.count_active.return_value = 0
    repo.create.return_value = _make_member()

    uc = CreateMember(repo=repo, fs=fs, data_root=Path("/data"))
    member = uc.execute("Ana García", "Backend")

    repo.create.assert_called_once_with(slug="ana-garcia", full_name="Ana García", role="Backend", color=MEMBER_COLOR_PALETTE[0])
    fs.initialize_member_dir.assert_called_once_with(Path("/data"), "ana-garcia", "Ana García", "Backend")
    assert member.slug == "ana-garcia"


def test_create_slug_collision():
    repo = MagicMock()
    fs = MagicMock()
    existing = _make_member(slug="ana-garcia")
    # First call (slug="ana-garcia") returns existing, second (slug="ana-garcia-2") returns None
    repo.get.side_effect = [existing, None]
    repo.count_active.return_value = 1
    repo.create.return_value = _make_member(slug="ana-garcia-2", color=MEMBER_COLOR_PALETTE[1])

    uc = CreateMember(repo=repo, fs=fs, data_root=Path("/data"))
    member = uc.execute("Ana García", "Backend")

    assert member.slug == "ana-garcia-2"


def test_color_round_robin():
    repo = MagicMock()
    fs = MagicMock()
    repo.get.return_value = None
    repo.count_active.return_value = 12  # wraps around
    expected_color = MEMBER_COLOR_PALETTE[0]
    repo.create.return_value = _make_member(color=expected_color)

    uc = CreateMember(repo=repo, fs=fs, data_root=Path("/data"))
    uc.execute("Ana García")

    _, kwargs = repo.create.call_args
    assert kwargs["color"] == expected_color
