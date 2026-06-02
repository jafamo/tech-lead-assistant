"""Tests de integración: SQLMemberRepository contra SQLite en memoria."""

import pytest
from sqlmodel import Session, SQLModel, create_engine

from tla.adapters.db.member_repo import SQLMemberRepository


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_create_and_get(session):
    repo = SQLMemberRepository(session)
    member = repo.create("ana-garcia", "Ana García", "Backend", "#4A90D9")
    assert member.id is not None
    fetched = repo.get("ana-garcia")
    assert fetched is not None
    assert fetched.full_name == "Ana García"
    assert fetched.color == "#4A90D9"


def test_list_active_empty(session):
    repo = SQLMemberRepository(session)
    assert repo.list_active() == []


def test_list_active_returns_only_active(session):
    repo = SQLMemberRepository(session)
    repo.create("ana", "Ana", None, "#4A90D9")
    repo.create("pedro", "Pedro", None, "#E67E22")
    repo.archive("pedro")
    active = repo.list_active()
    assert len(active) == 1
    assert active[0].slug == "ana"


def test_archive_and_reactivate(session):
    repo = SQLMemberRepository(session)
    repo.create("ana", "Ana", None, "#4A90D9")
    archived = repo.archive("ana")
    assert archived.status == "archived"
    assert archived.archived_at is not None
    active = repo.reactivate("ana")
    assert active.status == "active"
    assert active.archived_at is None


def test_count_active(session):
    repo = SQLMemberRepository(session)
    assert repo.count_active() == 0
    repo.create("ana", "Ana", None, "#4A90D9")
    repo.create("pedro", "Pedro", None, "#E67E22")
    assert repo.count_active() == 2
    repo.archive("ana")
    assert repo.count_active() == 1


def test_update_color(session):
    repo = SQLMemberRepository(session)
    repo.create("ana", "Ana", None, "#4A90D9")
    updated = repo.update_color("ana", "#E67E22")
    assert updated.color == "#E67E22"


def test_rename(session):
    repo = SQLMemberRepository(session)
    repo.create("ana", "Ana García", "Backend", "#4A90D9")
    renamed = repo.rename("ana", "Ana García Pérez", "Senior Backend")
    assert renamed.full_name == "Ana García Pérez"
    assert renamed.role == "Senior Backend"
    assert renamed.slug == "ana"
