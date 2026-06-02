"""Entrypoint NiceGUI — arranca el servidor."""

from __future__ import annotations

from tla.config import settings


def run() -> None:
    import nicegui.app
    from nicegui import ui

    # Importación diferida para evitar ciclos en tests
    from tla.adapters.ui.pages import login  # noqa: F401

    ui.run(
        host=settings.host,
        port=settings.port,
        title="Tech Lead Assistant",
        dark=None if settings.theme == "auto" else (settings.theme == "dark"),
        reload=False,
    )
