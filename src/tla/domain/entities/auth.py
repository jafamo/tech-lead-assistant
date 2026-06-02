"""Entidades de dominio para autenticación."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AuthSession:
    user_id: int
    started_at: datetime = field(default_factory=datetime.utcnow)
    last_activity_at: datetime = field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.last_activity_at = datetime.utcnow()

    def idle_minutes(self) -> float:
        delta = datetime.utcnow() - self.last_activity_at
        return delta.total_seconds() / 60
