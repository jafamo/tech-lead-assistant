"""Página de primer arranque (wizard): /first-run"""

from __future__ import annotations

import sys
from pathlib import Path

from nicegui import ui

from tla.config import settings


def _fde_recommendation() -> str:
    if sys.platform == "win32":
        return "Recomendamos activar BitLocker para proteger tus datos."
    elif sys.platform == "darwin":
        return "Recomendamos activar FileVault para proteger tus datos."
    else:
        return "Recomendamos usar LUKS o cifrado de disco completo para proteger tus datos."


@ui.page("/first-run")
async def first_run_page() -> None:
    from tla.auth import is_authenticated

    if is_authenticated():
        ui.navigate.to("/")
        return

    step = {"current": 1}

    with ui.card().classes("absolute-center w-[480px] shadow-lg"):
        title = ui.label("Bienvenido a TLA — Configuración inicial").classes(
            "text-xl font-bold text-center w-full mb-4"
        )

        # ── Paso 1: Crear cuenta ──────────────────────────────────────────
        with ui.column().classes("w-full gap-3") as step1_col:
            ui.label("Paso 1 de 2 — Crear cuenta").classes("text-sm text-gray-500")
            username_input = ui.input("Usuario").classes("w-full")
            password_input = ui.input(
                "Contraseña (mín. 8 caracteres)", password=True, password_toggle_button=True
            ).classes("w-full")
            confirm_input = ui.input(
                "Confirmar contraseña", password=True, password_toggle_button=True
            ).classes("w-full")
            error1 = ui.label("").classes("text-red-500 text-sm min-h-5")
            btn_next = ui.button("Siguiente →").classes("w-full mt-2")

        # ── Paso 2: Confirmar data_root ───────────────────────────────────
        with ui.column().classes("w-full gap-3") as step2_col:
            ui.label("Paso 2 de 2 — Directorio de datos").classes("text-sm text-gray-500")
            ui.label("Directorio donde se guardarán tus datos:").classes("text-sm")
            path_input = ui.input("TLA_DATA_ROOT", value=str(settings.data_root)).classes("w-full")
            error2 = ui.label("").classes("text-red-500 text-sm min-h-5")
            btn_finish = ui.button("Finalizar y comenzar").classes("w-full mt-2 bg-blue-600 text-white")

        step2_col.set_visibility(False)

        # ── Banner FDE ────────────────────────────────────────────────────
        with ui.column().classes("w-full gap-3") as fde_col:
            ui.icon("security", size="lg").classes("text-amber-500 self-center")
            ui.label("Seguridad del sistema").classes("text-lg font-semibold text-center w-full")
            ui.label(_fde_recommendation()).classes("text-sm text-center")
            ui.label(
                "TLA guarda los datos en texto plano para facilitar el uso con herramientas externas. "
                "El cifrado se delega al sistema operativo."
            ).classes("text-xs text-gray-400 text-center")
            btn_go = ui.button("Entendido — ir a Inicio").classes("w-full mt-2 bg-green-600 text-white")
            btn_go.on("click", lambda: ui.navigate.to("/"))

        fde_col.set_visibility(False)

        async def go_to_step2() -> None:
            if not username_input.value.strip():
                error1.set_text("El nombre de usuario no puede estar vacío.")
                return
            if len(password_input.value) < 8:
                error1.set_text("La contraseña debe tener al menos 8 caracteres.")
                return
            if password_input.value != confirm_input.value:
                error1.set_text("Las contraseñas no coinciden.")
                return
            error1.set_text("")
            step1_col.set_visibility(False)
            step2_col.set_visibility(True)

        async def finish() -> None:
            from tla.adapters.db.database import create_db_engine, init_db
            from tla.adapters.db.user_repo import SQLUserRepository
            from tla.adapters.fs.filesystem import LocalFileSystem
            from tla.domain.use_cases.create_user import CreateUser, UserAlreadyExistsError, PasswordTooShortError
            from tla.domain.use_cases.initialize_data_root import InitializeDataRoot
            from tla.domain.use_cases.publish_schema import PublishSchema
            from sqlmodel import Session

            data_root = Path(path_input.value.strip())
            if not data_root.is_absolute():
                error2.set_text("La ruta debe ser absoluta.")
                return

            try:
                init_db(settings.db_path)
                engine = create_db_engine(settings.db_path)
                with Session(engine) as session:
                    repo = SQLUserRepository(session)
                    CreateUser(repo=repo).execute(
                        username_input.value.strip(), password_input.value
                    )

                fs = LocalFileSystem()
                InitializeDataRoot(fs=fs).execute(data_root)

                schema_src = Path(__file__).parents[5] / "content.schema.json"
                if schema_src.exists():
                    PublishSchema(fs=fs).execute(schema_src, data_root)

                step2_col.set_visibility(False)
                fde_col.set_visibility(True)
                title.set_text("¡Configuración completada!")

            except (UserAlreadyExistsError, PasswordTooShortError) as e:
                error2.set_text(str(e))

        btn_next.on("click", go_to_step2)
        btn_finish.on("click", finish)
