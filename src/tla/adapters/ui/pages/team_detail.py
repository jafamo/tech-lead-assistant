"""Página de detalle de miembro: /team/{slug}"""

from __future__ import annotations

from nicegui import ui

from tla.app import require_auth

_MEETING_TYPE_LABELS = {
    "oneToOne": "1:1",
    "seguimiento": "Seguimiento",
    "feedback": "Feedback",
    "tecnica": "Técnica",
    "retro": "Retrospectiva",
}


def _get_deps(slug: str):
    from tla.adapters.db.database import create_db_engine
    from tla.adapters.db.member_repo import SQLMemberRepository
    from tla.adapters.db.meeting_repo import SQLMeetingRepository
    from tla.adapters.fs.transcription_fs import LocalTranscriptionFileSystem
    from tla.config import settings
    from sqlmodel import Session

    engine = create_db_engine(settings.db_path)
    session = Session(engine)
    return (
        SQLMemberRepository(session),
        SQLMeetingRepository(session),
        LocalTranscriptionFileSystem(),
        session,
        settings.data_root,
    )


@ui.page("/team/{slug}")
@require_auth
async def team_detail_page(slug: str) -> None:
    from tla.domain.exceptions import MemberNotFoundError, TLAError
    from tla.domain.use_cases.get_member import GetMember

    member_repo, meeting_repo, fs, session, data_root = _get_deps(slug)

    try:
        member = GetMember(repo=member_repo).execute(slug)
    except MemberNotFoundError:
        ui.label("Miembro no encontrado.").classes("text-red-500")
        ui.button("← Volver al equipo", on_click=lambda: ui.navigate.to("/team")).props("flat")
        return

    # ── Header ────────────────────────────────────────────────────────────────
    with ui.row().classes("items-center gap-3 mb-4"):
        ui.button(icon="arrow_back", on_click=lambda: ui.navigate.to("/team")).props("flat round")
        ui.element("div").style(
            f"width:18px;height:18px;border-radius:50%;background:{member.color}"
        )
        ui.label(member.full_name).classes("text-2xl font-bold")

    with ui.card().classes("w-full max-w-lg mb-6"):
        with ui.row().classes("gap-6"):
            with ui.column().classes("gap-1"):
                ui.label("Rol").classes("text-xs text-gray-500")
                ui.label(member.role or "—").classes("font-medium")
            with ui.column().classes("gap-1"):
                ui.label("Estado").classes("text-xs text-gray-500")
                ui.label(member.status.capitalize()).classes("font-medium")

    ui.separator().classes("my-4")

    # ── Sección transcripciones ───────────────────────────────────────────────
    with ui.row().classes("w-full items-center justify-between mb-3"):
        ui.label("Transcripciones").classes("text-lg font-semibold")
        upload_btn = ui.button("+ Subir", icon="upload_file")

    meetings_container = ui.column().classes("w-full gap-2")

    def _load_meetings():
        from tla.domain.use_cases.list_meetings import ListMeetings
        return ListMeetings(repo=meeting_repo).execute(member.id)

    def _render_meetings():
        meetings_container.clear()
        meetings = _load_meetings()
        with meetings_container:
            if not meetings:
                ui.label("Sin transcripciones.").classes("text-sm text-gray-400 py-2")
                return
            for m in meetings:
                type_label = _MEETING_TYPE_LABELS.get(m.meeting_type_slug, m.meeting_type_slug)
                with ui.card().classes("w-full p-3"):
                    with ui.row().classes("w-full items-center justify-between"):
                        with ui.column().classes("gap-0"):
                            ui.label(f"{m.meeting_date}  ·  {type_label}").classes("font-medium text-sm")
                            ui.label(m.title or "Sin título").classes("text-xs text-gray-500")
                        with ui.row().classes("gap-1"):
                            ui.button(
                                icon="edit",
                                on_click=lambda _, mid=m.id, rp=m.transcript_path: _open_editor(mid, rp),
                            ).props("flat dense round")
                            ui.button(
                                icon="delete",
                                on_click=lambda _, mid=m.id: _confirm_delete(mid),
                            ).props("flat dense round color=red")

    # ── Modal upload ──────────────────────────────────────────────────────────
    with ui.dialog() as upload_dialog, ui.card().classes("w-[520px]"):
        ui.label("Subir transcripción").classes("text-lg font-semibold mb-2")

        # Meeting type selector
        from tla.adapters.db.models import MeetingType as DBMeetingType
        from sqlmodel import select as sqlselect
        meeting_types = session.exec(sqlselect(DBMeetingType)).all()
        type_options = {mt.slug: mt.display_name for mt in meeting_types}
        type_select = ui.select(type_options, label="Tipo de reunión", value=list(type_options.keys())[0] if type_options else None).classes("w-full")

        date_input = ui.input("Fecha (YYYY-MM-DD)").classes("w-full")
        title_input = ui.input("Título (opcional)").classes("w-full")

        upload_log = ui.column().classes("w-full gap-1 mt-2")
        upload_status = ui.label("").classes("text-sm min-h-5")

        async def handle_upload(e) -> None:
            from tla.adapters.fs.transcription_fs import LocalTranscriptionFileSystem
            from tla.domain.use_cases.ingest_transcription import (
                IngestTranscription,
                extract_date_from_filename,
            )
            from tla.domain.exceptions import TLAError
            import datetime as dt

            # Resolve meeting_type_id
            mt = session.exec(
                sqlselect(DBMeetingType).where(DBMeetingType.slug == type_select.value)
            ).first()
            if mt is None:
                upload_status.classes("text-red-500")
                upload_status.set_text("Tipo de reunión no válido.")
                return

            # Resolve date
            raw_date = date_input.value.strip()
            if raw_date:
                try:
                    meeting_date = dt.date.fromisoformat(raw_date)
                except ValueError:
                    upload_status.classes("text-red-500")
                    upload_status.set_text("Fecha inválida. Usa YYYY-MM-DD.")
                    return
            else:
                meeting_date = extract_date_from_filename(e.name) or dt.date.today()
                date_input.set_value(str(meeting_date))

            content: bytes = e.content.read()
            uc = IngestTranscription(
                repo=meeting_repo,
                fs=LocalTranscriptionFileSystem(),
                data_root=data_root,
                member_slug=slug,
            )
            with upload_log:
                row = ui.row().classes("items-center gap-2 text-sm")
                with row:
                    spinner = ui.spinner(size="sm")
                    lbl = ui.label(e.name)
            try:
                uc.execute(
                    team_member_id=member.id,
                    meeting_type_id=mt.id,
                    meeting_type_slug=mt.slug,
                    meeting_date=meeting_date,
                    content=content,
                    filename=e.name,
                    title=title_input.value.strip() or None,
                )
                spinner.delete()
                lbl.classes("text-green-600")
                lbl.set_text(f"✓  {e.name}")
            except TLAError as exc:
                spinner.delete()
                lbl.classes("text-red-500")
                lbl.set_text(f"✗  {e.name} — {exc}")

        uploader = ui.upload(
            multiple=True,
            auto_upload=True,
            on_upload=handle_upload,
        ).props('accept=".txt,.md,.vtt,.srt" label="Arrastra ficheros o haz clic"').classes("w-full")

        async def _close_upload():
            upload_log.clear()
            upload_status.set_text("")
            date_input.set_value("")
            title_input.set_value("")
            uploader.reset()
            upload_dialog.close()
            _render_meetings()
            ui.notify("Transcripciones procesadas.", type="positive")

        with ui.row().classes("w-full justify-end gap-2 mt-3"):
            ui.button("Cerrar", on_click=_close_upload).classes("bg-blue-600 text-white")

    upload_btn.on("click", upload_dialog.open)

    # ── Modal editor ──────────────────────────────────────────────────────────
    with ui.dialog() as edit_dialog, ui.card().classes("w-[640px]"):
        edit_title = ui.label("Editar transcripción").classes("text-lg font-semibold mb-2")
        edit_area = ui.textarea().classes("w-full font-mono text-sm").props("rows=20")
        edit_rel_path_ref = {"value": "", "meeting_id": 0}
        edit_error = ui.label("").classes("text-red-500 text-sm min-h-5")

        async def _save_edit():
            try:
                fs.write_transcript_text(data_root, edit_rel_path_ref["value"], edit_area.value)
                # Re-index FTS
                meeting_repo.index_fts(
                    edit_rel_path_ref["meeting_id"],
                    edit_area.value,
                    slug,
                    "edited",
                )
                edit_dialog.close()
                edit_error.set_text("")
                ui.notify("Guardado.", type="positive")
            except Exception as exc:
                edit_error.set_text(str(exc))

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Cancelar", on_click=edit_dialog.close).props("flat")
            ui.button("Guardar", on_click=_save_edit).classes("bg-blue-600 text-white")

    def _open_editor(meeting_id: int, rel_path: str):
        try:
            content = fs.read_transcript(data_root, rel_path)
        except Exception:
            content = ""
        edit_rel_path_ref["value"] = rel_path
        edit_rel_path_ref["meeting_id"] = meeting_id
        edit_title.set_text(f"Editar — {rel_path.split('/')[-1]}")
        edit_area.set_value(content)
        edit_error.set_text("")
        edit_dialog.open()

    # ── Confirmación eliminar ─────────────────────────────────────────────────
    delete_id_ref = {"value": 0}

    with ui.dialog() as delete_dialog, ui.card().classes("w-80"):
        ui.label("¿Eliminar transcripción?").classes("text-lg font-semibold mb-2")
        ui.label("Se eliminará el fichero y su entrada en el índice.").classes("text-sm text-gray-600")
        delete_error = ui.label("").classes("text-red-500 text-sm min-h-5")

        async def _do_delete():
            from tla.domain.use_cases.delete_meeting import DeleteMeeting
            from tla.adapters.fs.transcription_fs import LocalTranscriptionFileSystem
            try:
                DeleteMeeting(
                    repo=meeting_repo,
                    fs=LocalTranscriptionFileSystem(),
                    data_root=data_root,
                ).execute(delete_id_ref["value"])
                delete_dialog.close()
                delete_error.set_text("")
                _render_meetings()
                ui.notify("Eliminado.", type="warning")
            except TLAError as exc:
                delete_error.set_text(str(exc))

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Cancelar", on_click=delete_dialog.close).props("flat")
            ui.button("Eliminar", on_click=_do_delete).classes("bg-red-600 text-white")

    def _confirm_delete(meeting_id: int):
        delete_id_ref["value"] = meeting_id
        delete_error.set_text("")
        delete_dialog.open()

    # ── Render inicial ────────────────────────────────────────────────────────
    _render_meetings()
