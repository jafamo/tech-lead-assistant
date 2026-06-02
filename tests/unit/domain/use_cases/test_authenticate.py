"""Tests unitarios de Authenticate."""

import pytest
import bcrypt
from unittest.mock import MagicMock

from tla.domain.use_cases.authenticate import Authenticate, AuthenticationError, NoUserError


def _hashed(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=4)).decode()


def _make_repo(password: str = "correct") -> MagicMock:
    repo = MagicMock()
    repo.get.return_value = MagicMock(id=1, password_hash=_hashed(password))
    return repo


def _make_session_store() -> MagicMock:
    store = MagicMock()
    store.create_session.return_value = MagicMock(user_id=1)
    return store


@pytest.mark.asyncio
async def test_correct_password_creates_session() -> None:
    uc = Authenticate(repo=_make_repo("correct"), session_store=_make_session_store())
    session = await uc.execute("correct")
    assert session is not None


@pytest.mark.asyncio
async def test_wrong_password_raises() -> None:
    uc = Authenticate(repo=_make_repo("correct"), session_store=_make_session_store())
    with pytest.raises(AuthenticationError):
        await uc.execute("wrong")


@pytest.mark.asyncio
async def test_failed_attempts_increments() -> None:
    uc = Authenticate(repo=_make_repo("correct"), session_store=_make_session_store())
    for _ in range(2):
        with pytest.raises(AuthenticationError):
            await uc.execute("wrong")
    assert uc.failed_attempts == 2


@pytest.mark.asyncio
async def test_success_resets_counter() -> None:
    uc = Authenticate(repo=_make_repo("correct"), session_store=_make_session_store())
    with pytest.raises(AuthenticationError):
        await uc.execute("wrong")
    await uc.execute("correct")
    assert uc.failed_attempts == 0


@pytest.mark.asyncio
async def test_backoff_seconds_calculated() -> None:
    store = _make_session_store()
    uc = Authenticate(repo=_make_repo("correct"), session_store=store)
    # Simular 3 fallos sin esperar realmente
    uc._failed_attempts = 3
    assert uc.backoff_seconds == 1
    uc._failed_attempts = 4
    assert uc.backoff_seconds == 2
    uc._failed_attempts = 9
    assert uc.backoff_seconds == 32  # capped at 32


@pytest.mark.asyncio
async def test_no_user_raises() -> None:
    repo = MagicMock()
    repo.get.return_value = None
    uc = Authenticate(repo=repo, session_store=_make_session_store())
    with pytest.raises(NoUserError):
        await uc.execute("any")
