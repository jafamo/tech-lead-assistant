"""Implementación SQLModel de MeetingRepository."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import text
from sqlmodel import Session, select

from tla.adapters.db.models import (
    Meeting as DBMeeting,
    MeetingParticipant,
    MeetingType,
    TeamMember as DBTeamMember,
)
from tla.domain.entities.meeting import Meeting
from tla.domain.ports.meeting_repository import MeetingRepository

_FTS_MAX_CHARS = 100_000


class SQLMeetingRepository(MeetingRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def _to_domain(self, record: DBMeeting) -> Meeting:
        # Resolve team_member via MeetingParticipant (single-participant meetings)
        participant = self._session.exec(
            select(MeetingParticipant).where(MeetingParticipant.meeting_id == record.id)
        ).first()
        member_id = participant.team_member_id if participant else 0
        member = self._session.get(DBTeamMember, member_id) if member_id else None
        meeting_type = self._session.get(MeetingType, record.meeting_type_id)
        return Meeting(
            id=record.id,  # type: ignore[arg-type]
            team_member_id=member_id,
            team_member_slug=member.slug if member else "",
            meeting_type_id=record.meeting_type_id,
            meeting_type_slug=meeting_type.slug if meeting_type else "",
            meeting_date=record.meeting_date,
            title=record.title,
            transcript_path=record.transcript_path,
            file_hash=record.file_hash or "",
            notes_path=record.notes_path,
            is_shared=record.is_shared,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    def create(
        self,
        team_member_id: int,
        meeting_type_id: int,
        meeting_date: date,
        transcript_path: str,
        file_hash: str,
        title: Optional[str] = None,
    ) -> Meeting:
        record = DBMeeting(
            meeting_type_id=meeting_type_id,
            meeting_date=meeting_date,
            transcript_path=transcript_path,
            file_hash=file_hash,
            title=title,
        )
        self._session.add(record)
        self._session.flush()  # get id before adding participant

        participant = MeetingParticipant(
            meeting_id=record.id,  # type: ignore[arg-type]
            team_member_id=team_member_id,
        )
        self._session.add(participant)
        self._session.commit()
        self._session.refresh(record)
        return self._to_domain(record)

    def get(self, meeting_id: int) -> Optional[Meeting]:
        record = self._session.get(DBMeeting, meeting_id)
        return self._to_domain(record) if record else None

    def list_for_member(self, team_member_id: int) -> list[Meeting]:
        # Find meeting_ids via MeetingParticipant
        participants = self._session.exec(
            select(MeetingParticipant).where(
                MeetingParticipant.team_member_id == team_member_id
            )
        ).all()
        meeting_ids = [p.meeting_id for p in participants]
        if not meeting_ids:
            return []
        records = self._session.exec(
            select(DBMeeting)
            .where(DBMeeting.id.in_(meeting_ids))  # type: ignore[attr-defined]
            .order_by(DBMeeting.meeting_date.desc())  # type: ignore[attr-defined]
        ).all()
        return [self._to_domain(r) for r in records]

    def hash_exists(self, file_hash: str) -> bool:
        return self._session.exec(
            select(DBMeeting).where(DBMeeting.file_hash == file_hash)
        ).first() is not None

    def delete(self, meeting_id: int) -> None:
        # Remove FTS entry
        self._session.exec(  # type: ignore[call-overload]
            text("DELETE FROM search_index WHERE file_path = :p"),
            params={"p": str(meeting_id)},
        )
        # Remove participant links
        participants = self._session.exec(
            select(MeetingParticipant).where(MeetingParticipant.meeting_id == meeting_id)
        ).all()
        for p in participants:
            self._session.delete(p)
        record = self._session.get(DBMeeting, meeting_id)
        if record:
            self._session.delete(record)
        self._session.commit()

    def index_fts(
        self, meeting_id: int, content: str, member_slug: str, doc_type: str
    ) -> None:
        truncated = content[:_FTS_MAX_CHARS]
        self._session.exec(  # type: ignore[call-overload]
            text(
                "INSERT INTO search_index(file_path, content, member_slug, doc_type)"
                " VALUES (:p, :c, :m, :d)"
            ),
            params={
                "p": str(meeting_id),
                "c": truncated,
                "m": member_slug,
                "d": doc_type,
            },
        )
        self._session.commit()

    def search_fts(self, query: str, member_slug: Optional[str] = None) -> list[Meeting]:
        sql = "SELECT file_path FROM search_index WHERE search_index MATCH :q"
        params: dict = {"q": query}
        if member_slug:
            sql += " AND member_slug = :m"
            params["m"] = member_slug
        rows = self._session.exec(text(sql), params=params).fetchall()  # type: ignore[call-overload]
        ids = [int(r[0]) for r in rows if str(r[0]).isdigit()]
        result = []
        for mid in ids:
            record = self._session.get(DBMeeting, mid)
            if record:
                result.append(self._to_domain(record))
        return result
