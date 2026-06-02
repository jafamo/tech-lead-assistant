"""Página de lock-screen: /login"""

from __future__ import annotations

import asyncio

from nicegui import ui

from tla.auth import InMemorySessionStore
from tla.domain.use_cases.authenticate import Authenticate, AuthenticationError, NoUserError


def _get_use_case() -> Authenticate:
    from tla.adapters.db.database import create_db_engine
    from tla.adapters.db.user_repo import SQLUserRepository
    from sqlmodel import Session
    from tla.config import settings

    engine = create_db_engine(settings.db_path)
    session = Session(engine)
    return Authenticate(
        repo=SQLUserRepository(session),
        session_store=InMemorySessionStore(),
    )


@ui.page("/login")
async def login_page() -> None:
    from tla.auth import is_authenticated

    if is_authenticated():
        ui.navigate.to("/")
        return

    uc = _get_use_case()

    with ui.card().classes("absolute-center w-96 shadow-lg"):
        ui.label("Tech Lead Assistant").classes("text-2xl font-bold text-center w-full mb-2")
        ui.label("Introduce tu contraseña para continuar").classes("text-sm text-gray-500 text-center w-full mb-4")

        password_input = ui.input(
            placeholder="Contraseña",
            password=True,
            password_toggle_button=True,
        ).classes("w-full")

        error_label = ui.label("").classes("text-red-500 text-sm min-h-5")
        countdown_label = ui.label("").classes("text-orange-500 text-sm min-h-5")
        submit_btn = ui.button("Desbloquear").classes("w-full mt-2")

        async def handle_login() -> None:
            backoff = uc.backoff_seconds
            if backoff > 0:
                submit_btn.disable()
                password_input.disable()
                for remaining in range(backoff, 0, -1):
                    countdown_label.set_text(f"Espera {remaining}s antes de intentarlo de nuevo…")
                    await asyncio.sleep(1)
                countdown_label.set_text("")
                submit_btn.enable()
                password_input.enable()

            try:
                await uc.execute(password_input.value)
                ui.navigate.to("/")
            except (AuthenticationError, NoUserError) as e:
                error_label.set_text(str(e))

        submit_btn.on("click", handle_login)
        password_input.on("keydown.enter", handle_login)
