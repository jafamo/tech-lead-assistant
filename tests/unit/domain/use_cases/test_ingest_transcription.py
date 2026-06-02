"""Tests unitarios: IngestTranscription."""

from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tla.domain.entities.meeting import Meeting
from tla.domain.exceptions import DuplicateTranscriptionError, UnsupportedFileFormatError
from tla.domain.use_cases.ingest_transcription import (
    IngestTranscription,
    extract_date_from_filename,
)


def _make_meeting() -> Meeting:
    return Meeting(
        id=1, team_member_id=1, team_member_slug="ana", meeting_type_id=1,
        meeting_type_slug="oneToOne", meeting_date=date(2024, 3, 15),
        title=None, transcript_path="ana/oneToOne/2024-03-15.transcript.txt",
        file_hash="abc123", notes_path=None, is_shared=False,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


def _uc(repo=None, fs=None):
    repo = repo or MagicMock()
    fs = fs or MagicMock()
    return IngestTranscription(repo=repo, fs=fs, data_root=Path("/data"), member_slug="ana")


def test_extract_date_from_filename():
    assert extract_date_from_filename("2024-03-15.transcript.txt") == date(2024, 3, 15)
    assert extract_date_from_filename("reunion.txt") is None


def test_ingest_success():
    repo, fs = MagicMock(), MagicMock()
    repo.hash_exists.return_value = False
    fs.write_transcript.return_value = "ana/oneToOne/2024-03-15.transcript.txt"
    repo.create.return_value = _make_meeting()

    meeting = _uc(repo, fs).execute(
        team_member_id=1, meeting_type_id=1, meeting_type_slug="oneToOne",
        meeting_date=date(2024, 3, 15), content=b"hola mundo",
        filename="2024-03-15.transcript.txt",
    )

    fs.write_transcript.assert_called_once()
    repo.create.assert_called_once()
    repo.index_fts.assert_called_once_with(1, "hola mundo", "ana", "oneToOne")
    assert meeting.id == 1


def test_ingest_duplicate():
    repo = MagicMock()
    repo.hash_exists.return_value = True

    with pytest.raises(DuplicateTranscriptionError):
        _uc(repo=repo).execute(
            team_member_id=1, meeting_type_id=1, meeting_type_slug="oneToOne",
            meeting_date=date(2024, 3, 15), content=b"contenido",
            filename="2024-03-15.transcript.txt",
        )


def test_ingest_unsupported_format():
    with pytest.raises(UnsupportedFileFormatError):
        _uc().execute(
            team_member_id=1, meeting_type_id=1, meeting_type_slug="oneToOne",
            meeting_date=date(2024, 3, 15), content=b"contenido",
            filename="reunion.pdf",
        )
