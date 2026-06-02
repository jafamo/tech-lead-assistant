"""Tests de integración: inicialización de DB SQLite."""

from pathlib import Path

import pytest
from sqlmodel import Session, select, text

from tla.adapters.db.database import create_db_engine, init_db
from tla.adapters.db.models import MeetingType


def test_init_db_creates_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    assert db_path.exists()


def test_init_db_seeds_meeting_types(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)

    engine = create_db_engine(db_path)
    with Session(engine) as session:
        types = session.exec(select(MeetingType)).all()
        slugs = {mt.slug for mt in types}

    assert slugs == {"oneToOne", "seguimiento", "feedback", "tecnica", "retro"}


def test_init_db_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    init_db(db_path)  # segunda vez no debe fallar ni duplicar seeds

    engine = create_db_engine(db_path)
    with Session(engine) as session:
        types = session.exec(select(MeetingType)).all()

    assert len(types) == 5


def test_fts_table_exists(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)

    engine = create_db_engine(db_path)
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='search_index'")
        ).fetchone()

    assert result is not None
