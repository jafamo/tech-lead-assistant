"""Use case: ingestar una transcripción en data_root."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

from tla.domain.entities.meeting import Meeting
from tla.domain.exceptions import DuplicateTranscriptionError, UnsupportedFileFormatError
from tla.domain.ports.meeting_repository import MeetingRepository
from tla.domain.ports.transcription_fs import TranscriptionFileSystemPort

ALLOWED_EXTENSIONS = {".txt", ".md", ".vtt", ".srt"}
_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def extract_date_from_filename(filename: str) -> Optional[date]:
    m = _DATE_RE.search(filename)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            return None
    return None


@dataclass
class IngestTranscription:
    repo: MeetingRepository
    fs: TranscriptionFileSystemPort
    data_root: Path
    member_slug: str

    def execute(
        self,
        team_member_id: int,
        meeting_type_id: int,
        meeting_type_slug: str,
        meeting_date: date,
        content: bytes,
        filename: str,
        title: Optional[str] = None,
    ) -> Meeting:
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise UnsupportedFileFormatError(
                f"Formato '{ext}' no soportado. Usa: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )

        file_hash = hashlib.md5(content).hexdigest()
        if self.repo.hash_exists(file_hash):
            raise DuplicateTranscriptionError(
                f"Ya existe una transcripción con el mismo contenido ({filename})."
            )

        rel_path = self.fs.write_transcript(
            self.data_root, self.member_slug, meeting_type_slug, meeting_date, ext, content
        )
        meeting = self.repo.create(
            team_member_id=team_member_id,
            meeting_type_id=meeting_type_id,
            meeting_date=meeting_date,
            transcript_path=rel_path,
            file_hash=file_hash,
            title=title,
        )
        content_text = content.decode("utf-8", errors="replace")
        self.repo.index_fts(meeting.id, content_text, self.member_slug, meeting_type_slug)
        return meeting
