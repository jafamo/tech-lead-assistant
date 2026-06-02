"""Página de ajustes: /settings"""

from __future__ import annotations

from nicegui import ui

from tla.app import require_auth


@ui.page("/settings")
@require_auth
async def settings_page() -> None:
    ui.label("Ajustes").classes("text-2xl font-bold mb-6")

    with ui.card().classes("w-full max-w-lg shadow"):
        ui.label("Cambiar contraseña").classes("text-lg font-semibold mb-4")

        current_input = ui.input(
            "Contraseña actual", password=True, password_toggle_button=True
        ).classes("w-full")
        new_input = ui.input(
            "Nueva contraseña (mín. 8 caracteres)", password=True, password_toggle_button=True
        ).classes("w-full")
        confirm_input = ui.input(
            "Confirmar nueva contraseña", password=True, password_toggle_button=True
        ).classes("w-full")

        feedback = ui.label("").classes("text-sm min-h-5")

        async def handle_change() -> None:
            from tla.adapters.db.database import create_db_engine
            from tla.adapters.db.user_repo import SQLUserRepository
            from tla.auth import get_current_session
            from tla.config import settings
            from tla.domain.use_cases.change_password import (
                ChangePassword,
                WrongCurrentPasswordError,
            )
            from sqlmodel import Session

            current_session = get_current_session()
            if current_session is None:
                ui.navigate.to("/login")
                return

            if len(new_input.value) < 8:
                feedback.classes("text-red-500", remove="text-green-600")
                feedback.set_text("La nueva contraseña debe tener al menos 8 caracteres.")
                return

            if new_input.value != confirm_input.value:
                feedback.classes("text-red-500", remove="text-green-600")
                feedback.set_text("Las contraseñas no coinciden.")
                return

            engine = create_db_engine(settings.db_path)
            with Session(engine) as session:
                repo = SQLUserRepository(session)
                try:
                    ChangePassword(repo=repo).execute(
                        current_session.user_id,
                        current_input.value,
                        new_input.value,
                    )
                    current_input.set_value("")
                    new_input.set_value("")
                    confirm_input.set_value("")
                    feedback.classes("text-green-600", remove="text-red-500")
                    feedback.set_text("Contraseña actualizada correctamente.")
                except WrongCurrentPasswordError as e:
                    feedback.classes("text-red-500", remove="text-green-600")
                    feedback.set_text(str(e))

        ui.button("Actualizar contraseña", on_click=handle_change).classes(
            "w-full mt-2 bg-blue-600 text-white"
        )
