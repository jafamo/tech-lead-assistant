"""Página de gestión del equipo: /team"""

from __future__ import annotations

from nicegui import ui

from tla.app import require_auth


def _get_deps():
    from tla.adapters.db.database import create_db_engine
    from tla.adapters.db.member_repo import SQLMemberRepository
    from tla.adapters.fs.member_fs import LocalMemberFileSystem
    from tla.config import settings
    from sqlmodel import Session

    engine = create_db_engine(settings.db_path)
    session = Session(engine)
    repo = SQLMemberRepository(session)
    fs = LocalMemberFileSystem()
    return repo, fs, session, settings.data_root


@ui.page("/team")
@require_auth
async def team_page() -> None:
    from tla.domain.use_cases.archive_member import ArchiveMember
    from tla.domain.use_cases.create_member import CreateMember
    from tla.domain.use_cases.list_members import ListMembers
    from tla.domain.use_cases.reactivate_member import ReactivateMember
    from tla.domain.use_cases.rename_member import RenameMember
    from tla.domain.use_cases.update_member_color import UpdateMemberColor
    from tla.domain.exceptions import TLAError

    repo, fs, session, data_root = _get_deps()

    def _load_members():
        return ListMembers(repo=repo).execute(include_archived=False)

    def _load_archived():
        from tla.domain.use_cases.list_members import ListMembers as LM
        all_m = LM(repo=repo).execute(include_archived=True)
        return [m for m in all_m if m.status == "archived"]

    # ── Header ────────────────────────────────────────────────────────────────
    with ui.row().classes("w-full items-center justify-between mb-4"):
        ui.label("Equipo").classes("text-2xl font-bold")
        add_btn = ui.button("+ Añadir miembro", icon="person_add")

    search_input = ui.input(placeholder="Buscar por nombre o rol…").classes("w-full mb-4")

    members_container = ui.column().classes("w-full gap-2")

    # ── Sección archivados ────────────────────────────────────────────────────
    archived_expansion = ui.expansion("Archivados", icon="archive").classes("w-full mt-4")

    def _render_archived():
        archived_expansion.clear()
        with archived_expansion:
            archived = _load_archived()
            if not archived:
                ui.label("No hay miembros archivados.").classes("text-sm text-gray-500 p-2")
                return
            archived_expansion.text = f"Archivados ({len(archived)})"
            with ui.column().classes("w-full gap-1 p-2"):
                for m in archived:
                    with ui.row().classes("w-full items-center justify-between"):
                        with ui.row().classes("items-center gap-2"):
                            ui.element("div").style(
                                f"width:12px;height:12px;border-radius:50%;background:{m.color}"
                            )
                            ui.label(m.full_name).classes("font-medium")
                        ui.button(
                            "Reactivar",
                            on_click=lambda _, s=m.slug: _reactivate(s),
                        ).classes("text-xs").props("flat dense")

    def _render_members(filter_text: str = ""):
        members_container.clear()
        members = _load_members()
        if filter_text:
            ft = filter_text.lower()
            members = [
                m for m in members
                if ft in m.full_name.lower() or (m.role and ft in m.role.lower())
            ]
        with members_container:
            if not members:
                ui.label("Sin miembros activos.").classes("text-sm text-gray-400")
                return
            for m in members:
                with ui.card().classes("w-full p-3"):
                    with ui.row().classes("w-full items-center justify-between"):
                        with ui.row().classes("items-center gap-3 cursor-pointer").on(
                            "click", lambda _, s=m.slug: ui.navigate.to(f"/team/{s}")
                        ):
                            ui.element("div").style(
                                f"width:14px;height:14px;border-radius:50%;background:{m.color};flex-shrink:0"
                            )
                            with ui.column().classes("gap-0"):
                                ui.label(m.full_name).classes("font-semibold leading-tight")
                                ui.label(m.role or "—").classes("text-xs text-gray-500")
                        _member_menu(m.slug, m.full_name, m.role, m.color)

    def _member_menu(slug: str, full_name: str, role, color: str):
        with ui.button(icon="more_vert").props("flat dense round"):
            with ui.menu():
                ui.menu_item("Renombrar", on_click=lambda: _open_rename_modal(slug, full_name, role))
                ui.menu_item("Cambiar color", on_click=lambda: _open_color_picker(slug, color))
                ui.menu_item(
                    "Archivar",
                    on_click=lambda: _confirm_archive(slug, full_name),
                ).classes("text-red-500")

    # ── Modal Añadir ──────────────────────────────────────────────────────────
    with ui.dialog() as add_dialog, ui.card().classes("w-96"):
        ui.label("Añadir miembro").classes("text-lg font-semibold mb-2")
        name_input = ui.input("Nombre completo *").classes("w-full")
        role_input = ui.input("Rol (opcional)").classes("w-full")
        add_error = ui.label("").classes("text-red-500 text-sm min-h-5")

        async def _do_create():
            if not name_input.value.strip():
                add_error.set_text("El nombre es obligatorio.")
                return
            try:
                CreateMember(repo=repo, fs=fs, data_root=data_root).execute(
                    name_input.value.strip(), role_input.value.strip() or None
                )
                add_dialog.close()
                name_input.set_value("")
                role_input.set_value("")
                add_error.set_text("")
                _render_members()
                _render_archived()
                ui.notify("Miembro creado correctamente.", type="positive")
            except TLAError as e:
                add_error.set_text(str(e))

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Cancelar", on_click=add_dialog.close).props("flat")
            ui.button("Guardar", on_click=_do_create).classes("bg-blue-600 text-white")

    add_btn.on("click", add_dialog.open)

    # ── Modal Renombrar ───────────────────────────────────────────────────────
    with ui.dialog() as rename_dialog, ui.card().classes("w-96"):
        ui.label("Renombrar miembro").classes("text-lg font-semibold mb-2")
        rename_slug_ref = {"value": ""}
        rename_name_input = ui.input("Nombre completo").classes("w-full")
        rename_role_input = ui.input("Rol").classes("w-full")
        rename_error = ui.label("").classes("text-red-500 text-sm min-h-5")

        async def _do_rename():
            try:
                RenameMember(repo=repo).execute(
                    rename_slug_ref["value"],
                    rename_name_input.value.strip(),
                    rename_role_input.value.strip() or None,
                )
                rename_dialog.close()
                rename_error.set_text("")
                _render_members(search_input.value)
                ui.notify("Miembro renombrado.", type="positive")
            except TLAError as e:
                rename_error.set_text(str(e))

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Cancelar", on_click=rename_dialog.close).props("flat")
            ui.button("Guardar", on_click=_do_rename).classes("bg-blue-600 text-white")

    def _open_rename_modal(slug: str, full_name: str, role):
        rename_slug_ref["value"] = slug
        rename_name_input.set_value(full_name)
        rename_role_input.set_value(role or "")
        rename_error.set_text("")
        rename_dialog.open()

    # ── Color picker ─────────────────────────────────────────────────────────
    _PALETTE = [
        "#4A90D9", "#E67E22", "#27AE60", "#8E44AD", "#E74C3C",
        "#1ABC9C", "#F39C12", "#2980B9", "#D35400", "#16A085",
        "#C0392B", "#7F8C8D",
    ]

    with ui.dialog() as color_dialog, ui.card().classes("w-80"):
        ui.label("Cambiar color").classes("text-lg font-semibold mb-2")
        color_slug_ref = {"value": ""}
        color_input = ui.color_input(label="Color").classes("w-full")
        ui.label("Paleta sugerida:").classes("text-xs text-gray-500 mt-2")
        with ui.row().classes("flex-wrap gap-1 mt-1"):
            for c in _PALETTE:
                ui.element("div").style(
                    f"width:24px;height:24px;border-radius:4px;background:{c};cursor:pointer"
                ).on("click", lambda _, col=c: color_input.set_value(col))
        color_error = ui.label("").classes("text-red-500 text-sm min-h-5")

        async def _do_color():
            try:
                UpdateMemberColor(repo=repo).execute(color_slug_ref["value"], color_input.value)
                color_dialog.close()
                color_error.set_text("")
                _render_members(search_input.value)
                ui.notify("Color actualizado.", type="positive")
            except TLAError as e:
                color_error.set_text(str(e))

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Cancelar", on_click=color_dialog.close).props("flat")
            ui.button("Aplicar", on_click=_do_color).classes("bg-blue-600 text-white")

    def _open_color_picker(slug: str, current_color: str):
        color_slug_ref["value"] = slug
        color_input.set_value(current_color)
        color_error.set_text("")
        color_dialog.open()

    # ── Confirmación archivar ─────────────────────────────────────────────────
    archive_slug_ref = {"value": "", "name": ""}

    with ui.dialog() as archive_dialog, ui.card().classes("w-96"):
        ui.label("¿Archivar miembro?").classes("text-lg font-semibold mb-2")
        archive_msg = ui.label("").classes("text-sm text-gray-600 mb-4")
        archive_error = ui.label("").classes("text-red-500 text-sm min-h-5")

        async def _do_archive():
            try:
                ArchiveMember(repo=repo, fs=fs, data_root=data_root).execute(
                    archive_slug_ref["value"]
                )
                archive_dialog.close()
                archive_error.set_text("")
                _render_members(search_input.value)
                _render_archived()
                ui.notify("Miembro archivado.", type="warning")
            except TLAError as e:
                archive_error.set_text(str(e))

        with ui.row().classes("w-full justify-end gap-2"):
            ui.button("Cancelar", on_click=archive_dialog.close).props("flat")
            ui.button("Archivar", on_click=_do_archive).classes("bg-red-600 text-white")

    def _confirm_archive(slug: str, full_name: str):
        archive_slug_ref["value"] = slug
        archive_slug_ref["name"] = full_name
        archive_msg.set_text(
            f"Los datos de {full_name} se moverán a _archive/. Podrás reactivarlo después."
        )
        archive_error.set_text("")
        archive_dialog.open()

    def _reactivate(slug: str):
        try:
            ReactivateMember(repo=repo, fs=fs, data_root=data_root).execute(slug)
            _render_members(search_input.value)
            _render_archived()
            ui.notify("Miembro reactivado.", type="positive")
        except TLAError as e:
            ui.notify(str(e), type="negative")

    # ── Búsqueda ──────────────────────────────────────────────────────────────
    search_input.on("input", lambda: _render_members(search_input.value))

    # ── Render inicial ────────────────────────────────────────────────────────
    _render_members()
    _render_archived()
