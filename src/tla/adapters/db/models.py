"""Modelos SQLModel — índice SQLite de TLA."""

from datetime import date, datetime, time
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MeetingParticipant(SQLModel, table=True):
    meeting_id: int = Field(foreign_key="meeting.id", primary_key=True)
    team_member_id: int = Field(foreign_key="teammember.id", primary_key=True)


class ReportMeeting(SQLModel, table=True):
    report_id: int = Field(foreign_key="report.id", primary_key=True)
    meeting_id: int = Field(foreign_key="meeting.id", primary_key=True)


class TeamMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True)
    full_name: str
    role: Optional[str] = None
    start_date: Optional[date] = None
    notes: Optional[str] = None
    color: str  # hex, ej. '#4A90D9'
    status: str = Field(default="active")  # active | archived
    archived_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_indexed_at: Optional[datetime] = None

    meetings: list["Meeting"] = Relationship(
        back_populates="participants",
        link_model=MeetingParticipant,
    )
    reports: list["Report"] = Relationship(back_populates="team_member")
    scheduled_meetings: list["ScheduledMeeting"] = Relationship(back_populates="team_member")


class MeetingType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True)
    display_name: str
    icon: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    meetings: list["Meeting"] = Relationship(back_populates="meeting_type")
    scheduled_meetings: list["ScheduledMeeting"] = Relationship(back_populates="meeting_type")


class Meeting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    meeting_type_id: int = Field(foreign_key="meetingtype.id")
    meeting_date: date
    title: Optional[str] = None
    transcript_path: str
    notes_path: Optional[str] = None
    is_shared: bool = Field(default=False)
    file_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    meeting_type: Optional[MeetingType] = Relationship(back_populates="meetings")
    participants: list[TeamMember] = Relationship(
        back_populates="meetings",
        link_model=MeetingParticipant,
    )
    reports: list["Report"] = Relationship(
        back_populates="source_meetings",
        link_model=ReportMeeting,
    )


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_member_id: int = Field(foreign_key="teammember.id", index=True)
    period_label: str
    period_start: date
    period_end: date
    generation_mode: str  # llm | manual | imported
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    version: int = Field(default=1)
    status: str = Field(default="draft")  # draft | final | schema_invalid
    folder_path: str
    content_hash: Optional[str] = None
    schema_valid: bool = Field(default=True)
    schema_errors: Optional[str] = None
    charts_generated: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

    team_member: Optional[TeamMember] = Relationship(back_populates="reports")
    source_meetings: list[Meeting] = Relationship(
        back_populates="reports",
        link_model=ReportMeeting,
    )


class ScheduledMeeting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_member_id: Optional[int] = Field(default=None, foreign_key="teammember.id")
    meeting_type_id: Optional[int] = Field(default=None, foreign_key="meetingtype.id")
    title: str
    scheduled_date: date
    scheduled_time: Optional[time] = None
    duration_minutes: int = Field(default=30)
    recurrence: Optional[str] = None  # weekly | biweekly | monthly
    recurrence_end_date: Optional[date] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    status: str = Field(default="pending")  # pending | completed | cancelled
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    team_member: Optional[TeamMember] = Relationship(back_populates="scheduled_meetings")
    meeting_type: Optional[MeetingType] = Relationship(back_populates="scheduled_meetings")
