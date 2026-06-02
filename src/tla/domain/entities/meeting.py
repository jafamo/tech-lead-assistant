"""Entidad de dominio: Meeting."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Meeting:
    id: int
    team_member_id: int
    team_member_slug: str
    meeting_type_id: int
    meeting_type_slug: str
    meeting_date: date
    title: Optional[str]
    transcript_path: str   # relativo a data_root
    file_hash: str
    notes_path: Optional[str]
    is_shared: bool
    created_at: datetime
    updated_at: datetime
