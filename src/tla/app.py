"""Entrypoint NiceGUI — arranca el servidor."""

from __future__ import annotations

from functools import wraps
from typing import Callable

from nicegui import ui

from tla.config import settings


def require_auth(func: Callable) -> Callable:
    """Decorator: redirige a /login si no hay sesión activa."""
    @wraps(func)
    async def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        from tla.auth import is_authenticated
        if not is_authenticated():
            ui.navigate.to("/login")
            return
        return await func(*args, **kwargs)
    return wrapper


def run() -> None:
    from nicegui import app as _app
    from tla.adapters.db.database import init_db

    @_app.on_startup
    def _startup() -> None:
        init_db(settings.db_path)

    from tla.adapters.ui.pages import login  # noqa: F401
    from tla.adapters.ui.pages import first_run  # noqa: F401
    from tla.adapters.ui.pages import settings as _settings_page  # noqa: F401
    from tla.adapters.ui.pages import team as _team_page  # noqa: F401
    from tla.adapters.ui.pages import team_detail as _team_detail_page  # noqa: F401

    @ui.page("/")
    async def index() -> None:
        from tla.adapters.db.database import create_db_engine
        from tla.adapters.db.user_repo import SQLUserRepository
        from tla.auth import is_authenticated
        from sqlmodel import Session

        engine = create_db_engine(settings.db_path)
        with Session(engine) as session:
            from tla.domain.use_cases.check_first_run import CheckFirstRun
            is_first_run = CheckFirstRun(repo=SQLUserRepository(session)).execute()

        if is_first_run:
            ui.navigate.to("/first-run")
        elif not is_authenticated():
            ui.navigate.to("/login")
        else:
            ui.label("Tech Lead Assistant").classes("text-2xl font-bold mb-4")
            ui.button("Ver equipo →", on_click=lambda: ui.navigate.to("/team")).classes("mt-2")

    ui.run(
        host=settings.host,
        port=settings.port,
        title="Tech Lead Assistant",
        dark=None if settings.theme == "auto" else (settings.theme == "dark"),
        reload=False,
    )
