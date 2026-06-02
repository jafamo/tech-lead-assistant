"""Genera y regenera AGENTS.md en data_root desde plantilla Jinja2."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, PackageLoader

from tla.adapters.fs.writer import atomic_write_text

_USER_NOTES_MARKER = "## User notes"


def _get_env() -> Environment:
    return Environment(
        loader=PackageLoader("tla", "templates"),
        autoescape=False,
        keep_trailing_newline=True,
    )


def generate_agents_md(data_root: Path, version: str = "0.1.0") -> Path:
    """Genera data_root/AGENTS.md. Si ya existe, preserva la sección 'User notes'."""
    dst = data_root / "AGENTS.md"
    user_notes = _extract_user_notes(dst)

    env = _get_env()
    template = env.get_template("AGENTS.md.j2")
    content = template.render(version=version, user_notes=user_notes)
    atomic_write_text(dst, content)
    return dst


def _extract_user_notes(path: Path) -> str:
    """Extrae el bloque posterior a '## User notes' si existe."""
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    idx = text.find(_USER_NOTES_MARKER)
    if idx == -1:
        return ""
    return text[idx + len(_USER_NOTES_MARKER):].strip()
