"""Entidad de dominio: TeamMember."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

MEMBER_COLOR_PALETTE = [
    "#4A90D9", "#E67E22", "#27AE60", "#8E44AD", "#E74C3C",
    "#1ABC9C", "#F39C12", "#2980B9", "#D35400", "#16A085",
    "#C0392B", "#7F8C8D",
]


@dataclass
class TeamMember:
    id: int
    slug: str
    full_name: str
    role: Optional[str]
    color: str
    status: str  # "active" | "archived"
    start_date: Optional[date]
    archived_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
