"""Resolución centralizada de rutas del filesystem TLA."""

from __future__ import annotations

from pathlib import Path

from tla.config import Settings


def member_dir(settings: Settings, slug: str) -> Path:
    return settings.data_root / slug


def member_archive_dir(settings: Settings, slug: str) -> Path:
    return settings.data_root / "_archive" / slug


def member_profile_path(settings: Settings, slug: str) -> Path:
    return member_dir(settings, slug) / "profile" / "profile.md"


def member_meeting_dir(settings: Settings, slug: str, meeting_type: str) -> Path:
    return member_dir(settings, slug) / meeting_type


def report_dir(settings: Settings, slug: str, period: str, version: int, mode: str) -> Path:
    return member_dir(settings, slug) / "reports" / f"{period}_v{version}_{mode}"


def staging_dir(settings: Settings, slug: str) -> Path:
    assert settings.reports_import_dir is not None
    return settings.reports_import_dir / slug


def stats_current_dir(settings: Settings) -> Path:
    assert settings.stats_dir is not None
    return settings.stats_dir / "current"


def stats_history_dir(settings: Settings, period: str) -> Path:
    assert settings.stats_history_dir is not None
    return settings.stats_history_dir / period


def published_schema_path(settings: Settings) -> Path:
    return settings.data_root / "_published_schema" / "content.schema.json"
