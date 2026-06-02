"""Tests de integración: SQLUserRepository contra SQLite en memoria."""

import pytest
from sqlmodel import Session, SQLModel, create_engine

from tla.adapters.db.user_repo import SQLUserRepository


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_create_and_get(session) -> None:
    repo = SQLUserRepository(session)
    user = repo.create("admin", "hash123")
    assert user.id is not None
    fetched = repo.get()
    assert fetched is not None
    assert fetched.username == "admin"


def test_exists_false_when_empty(session) -> None:
    repo = SQLUserRepository(session)
    assert repo.exists() is False


def test_exists_true_after_create(session) -> None:
    repo = SQLUserRepository(session)
    repo.create("admin", "hash123")
    assert repo.exists() is True


def test_update_password(session) -> None:
    repo = SQLUserRepository(session)
    user = repo.create("admin", "oldhash")
    repo.update_password(user.id, "newhash")
    updated = repo.get()
    assert updated is not None
    assert updated.password_hash == "newhash"
