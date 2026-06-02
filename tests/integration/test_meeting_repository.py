"""Tests de integración: SQLMeetingRepository contra SQLite en memoria."""

from datetime import date

import pytest
from sqlmodel import Session, SQLModel, create_engine

from tla.adapters.db.meeting_repo import SQLMeetingRepository
from tla.adapters.db.models import MeetingType, TeamMember


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    # FTS5 virtual table
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text(
            "CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5"
            "(file_path, content, member_slug, doc_type)"
        ))
        conn.commit()
    with Session(engine) as s:
        # Seed member and meeting type
        member = TeamMember(slug="ana", full_name="Ana García", color="#4A90D9")
        mt = MeetingType(slug="oneToOne", display_name="1:1")
        s.add(member)
        s.add(mt)
        s.commit()
        s.refresh(member)
        s.refresh(mt)
        yield s, member.id, mt.id


def test_create_and_get(session):
    s, member_id, type_id = session
    repo = SQLMeetingRepository(s)
    meeting = repo.create(member_id, type_id, date(2024, 3, 15),
                          "ana/oneToOne/2024-03-15.transcript.txt", "hash1")
    assert meeting.id is not None
    fetched = repo.get(meeting.id)
    assert fetched is not None
    assert fetched.meeting_date == date(2024, 3, 15)
    assert fetched.team_member_slug == "ana"


def test_hash_exists(session):
    s, member_id, type_id = session
    repo = SQLMeetingRepository(s)
    assert repo.hash_exists("nonexistent") is False
    repo.create(member_id, type_id, date(2024, 3, 15),
                "ana/oneToOne/2024-03-15.transcript.txt", "myhash")
    assert repo.hash_exists("myhash") is True


def test_list_for_member(session):
    s, member_id, type_id = session
    repo = SQLMeetingRepository(s)
    assert repo.list_for_member(member_id) == []
    repo.create(member_id, type_id, date(2024, 3, 15),
                "ana/oneToOne/2024-03-15.transcript.txt", "h1")
    repo.create(member_id, type_id, date(2024, 4, 1),
                "ana/oneToOne/2024-04-01.transcript.txt", "h2")
    results = repo.list_for_member(member_id)
    assert len(results) == 2
    # Ordered desc
    assert results[0].meeting_date >= results[1].meeting_date


def test_delete(session):
    s, member_id, type_id = session
    repo = SQLMeetingRepository(s)
    meeting = repo.create(member_id, type_id, date(2024, 3, 15),
                          "ana/oneToOne/2024-03-15.transcript.txt", "h1")
    repo.delete(meeting.id)
    assert repo.get(meeting.id) is None


def test_index_and_search_fts(session):
    s, member_id, type_id = session
    repo = SQLMeetingRepository(s)
    meeting = repo.create(member_id, type_id, date(2024, 3, 15),
                          "ana/oneToOne/2024-03-15.transcript.txt", "h1")
    repo.index_fts(meeting.id, "hablamos sobre el rendimiento del equipo", "ana", "oneToOne")

    results = repo.search_fts("rendimiento")
    assert len(results) == 1
    assert results[0].id == meeting.id

    # Filter by member
    results2 = repo.search_fts("rendimiento", member_slug="ana")
    assert len(results2) == 1

    # No match
    assert repo.search_fts("inexistente") == []
