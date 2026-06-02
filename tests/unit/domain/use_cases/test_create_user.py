"""Tests unitarios de CreateUser."""

import pytest
from unittest.mock import MagicMock

import bcrypt

from tla.domain.use_cases.create_user import CreateUser, UserAlreadyExistsError, PasswordTooShortError


def _make_repo(exists: bool = False) -> MagicMock:
    repo = MagicMock()
    repo.exists.return_value = exists
    repo.create.side_effect = lambda username, password_hash: MagicMock(
        id=1, username=username, password_hash=password_hash
    )
    return repo


def test_create_user_success() -> None:
    repo = _make_repo(exists=False)
    user = CreateUser(repo=repo).execute("admin", "securepass")
    repo.create.assert_called_once()
    stored_hash = repo.create.call_args.kwargs["password_hash"]
    assert bcrypt.checkpw(b"securepass", stored_hash.encode())


def test_create_user_hashes_password() -> None:
    repo = _make_repo(exists=False)
    CreateUser(repo=repo).execute("admin", "securepass")
    stored_hash = repo.create.call_args.kwargs["password_hash"]
    assert stored_hash != "securepass"


def test_create_user_duplicate_rejected() -> None:
    repo = _make_repo(exists=True)
    with pytest.raises(UserAlreadyExistsError):
        CreateUser(repo=repo).execute("admin", "securepass")
    repo.create.assert_not_called()


def test_create_user_short_password_rejected() -> None:
    repo = _make_repo(exists=False)
    with pytest.raises(PasswordTooShortError):
        CreateUser(repo=repo).execute("admin", "short")
    repo.create.assert_not_called()


def test_create_user_exactly_min_length_accepted() -> None:
    repo = _make_repo(exists=False)
    CreateUser(repo=repo).execute("admin", "12345678")  # 8 chars — OK
    repo.create.assert_called_once()
