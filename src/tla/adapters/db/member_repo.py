"""Implementación SQLModel de MemberRepository."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Session, func, select

from tla.adapters.db.models import TeamMember as DBTeamMember
from tla.domain.entities.member import TeamMember
from tla.domain.ports.member_repository import MemberRepository


class SQLMemberRepository(MemberRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def _to_domain(self, r: DBTeamMember) -> TeamMember:
        return TeamMember(
            id=r.id,  # type: ignore[arg-type]
            slug=r.slug,
            full_name=r.full_name,
            role=r.role,
            color=r.color,
            status=r.status,
            start_date=r.start_date,
            archived_at=r.archived_at,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )

    def create(self, slug: str, full_name: str, role: Optional[str], color: str) -> TeamMember:
        record = DBTeamMember(slug=slug, full_name=full_name, role=role, color=color)
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return self._to_domain(record)

    def get(self, slug: str) -> Optional[TeamMember]:
        record = self._session.exec(
            select(DBTeamMember).where(DBTeamMember.slug == slug)
        ).first()
        return self._to_domain(record) if record else None

    def list_active(self) -> list[TeamMember]:
        records = self._session.exec(
            select(DBTeamMember).where(DBTeamMember.status == "active")
        ).all()
        return [self._to_domain(r) for r in records]

    def list_all(self) -> list[TeamMember]:
        records = self._session.exec(select(DBTeamMember)).all()
        return [self._to_domain(r) for r in records]

    def count_active(self) -> int:
        result = self._session.exec(
            select(func.count()).select_from(DBTeamMember).where(DBTeamMember.status == "active")
        ).one()
        return result or 0

    def rename(self, slug: str, new_full_name: str, new_role: Optional[str]) -> TeamMember:
        record = self._session.exec(
            select(DBTeamMember).where(DBTeamMember.slug == slug)
        ).one()
        record.full_name = new_full_name
        record.role = new_role
        record.updated_at = datetime.utcnow()
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return self._to_domain(record)

    def archive(self, slug: str) -> TeamMember:
        record = self._session.exec(
            select(DBTeamMember).where(DBTeamMember.slug == slug)
        ).one()
        record.status = "archived"
        record.archived_at = datetime.utcnow()
        record.updated_at = datetime.utcnow()
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return self._to_domain(record)

    def reactivate(self, slug: str) -> TeamMember:
        record = self._session.exec(
            select(DBTeamMember).where(DBTeamMember.slug == slug)
        ).one()
        record.status = "active"
        record.archived_at = None
        record.updated_at = datetime.utcnow()
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return self._to_domain(record)

    def update_color(self, slug: str, color: str) -> TeamMember:
        record = self._session.exec(
            select(DBTeamMember).where(DBTeamMember.slug == slug)
        ).one()
        record.color = color
        record.updated_at = datetime.utcnow()
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return self._to_domain(record)
