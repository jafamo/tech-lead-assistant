"""Tests unitarios de CheckFirstRun e InvalidateSession."""

from unittest.mock import MagicMock

from tla.domain.use_cases.check_first_run import CheckFirstRun
from tla.domain.use_cases.invalidate_session import InvalidateSession


def test_first_run_true_when_no_user() -> None:
    repo = MagicMock()
    repo.exists.return_value = False
    assert CheckFirstRun(repo=repo).execute() is True


def test_first_run_false_when_user_exists() -> None:
    repo = MagicMock()
    repo.exists.return_value = True
    assert CheckFirstRun(repo=repo).execute() is False


def test_invalidate_session_calls_store() -> None:
    store = MagicMock()
    InvalidateSession(session_store=store).execute()
    store.invalidate.assert_called_once()
