"""Inicialización de la base de datos SQLite."""

from __future__ import annotations

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select, text

from tla.adapters.db.models import (  # noqa: F401 — ensure all models are registered in metadata
    Meeting,
    MeetingParticipant,
    MeetingType,
    Report,
    ReportMeeting,
    ScheduledMeeting,
    TeamMember,
    User,
)

_MEETING_TYPES_SEED = [
    {"slug": "oneToOne", "display_name": "1:1", "icon": "message-circle"},
    {"slug": "seguimiento", "display_name": "Seguimiento", "icon": "activity"},
    {"slug": "feedback", "display_name": "Feedback", "icon": "thumbs-up"},
    {"slug": "tecnica", "display_name": "Técnica", "icon": "code"},
    {"slug": "retro", "display_name": "Retrospectiva", "icon": "rotate-ccw"},
]


def create_db_engine(db_path: Path):  # type: ignore[return]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    url = f"sqlite:///{db_path}"
    return create_engine(url, connect_args={"check_same_thread": False})


def init_db(db_path: Path) -> None:
    """Crea tablas, FTS5 y seed de meeting_type si no existen."""
    engine = create_db_engine(db_path)
    SQLModel.metadata.create_all(engine)
    _create_fts(engine)

    with Session(engine) as session:
        _seed_meeting_types(session)
        session.commit()


def _create_fts(engine) -> None:  # type: ignore[type-arg]
    fts_ddl = """
    CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
        file_path,
        content,
        member_slug,
        doc_type
    );
    """
    with engine.connect() as conn:
        conn.execute(text(fts_ddl))
        conn.commit()


def _seed_meeting_types(session: Session) -> None:
    for mt_data in _MEETING_TYPES_SEED:
        existing = session.exec(
            select(MeetingType).where(MeetingType.slug == mt_data["slug"])
        ).first()
        if not existing:
            session.add(MeetingType(**mt_data))
