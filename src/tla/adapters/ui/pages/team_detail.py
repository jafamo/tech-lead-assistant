"""Página de detalle de miembro: /team/{slug}"""

from __future__ import annotations

from nicegui import ui

from tla.app import require_auth


@ui.page("/team/{slug}")
@require_auth
async def team_detail_page(slug: str) -> None:
    from tla.adapters.db.database import create_db_engine
    from tla.adapters.db.member_repo import SQLMemberRepository
    from tla.config import settings
    from tla.domain.exceptions import MemberNotFoundError
    from tla.domain.use_cases.get_member import GetMember
    from sqlmodel import Session

    engine = create_db_engine(settings.db_path)
    with Session(engine) as session:
        repo = SQLMemberRepository(session)
        try:
            member = GetMember(repo=repo).execute(slug)
        except MemberNotFoundError:
            ui.label("Miembro no encontrado.").classes("text-red-500")
            ui.button("← Volver al equipo", on_click=lambda: ui.navigate.to("/team")).props("flat")
            return

    with ui.row().classes("items-center gap-3 mb-6"):
        ui.button(icon="arrow_back", on_click=lambda: ui.navigate.to("/team")).props("flat round")
        ui.element("div").style(
            f"width:18px;height:18px;border-radius:50%;background:{member.color}"
        )
        ui.label(member.full_name).classes("text-2xl font-bold")

    with ui.card().classes("w-full max-w-lg"):
        with ui.row().classes("gap-6"):
            with ui.column().classes("gap-1"):
                ui.label("Rol").classes("text-xs text-gray-500")
                ui.label(member.role or "—").classes("font-medium")
            with ui.column().classes("gap-1"):
                ui.label("Estado").classes("text-xs text-gray-500")
                ui.label(member.status.capitalize()).classes("font-medium")
            with ui.column().classes("gap-1"):
                ui.label("Color").classes("text-xs text-gray-500")
                with ui.row().classes("items-center gap-2"):
                    ui.element("div").style(
                        f"width:14px;height:14px;border-radius:3px;background:{member.color}"
                    )
                    ui.label(member.color).classes("font-mono text-sm")

    ui.separator().classes("my-6")
    ui.label("Reuniones y reports — próximamente").classes("text-gray-400 text-sm")
