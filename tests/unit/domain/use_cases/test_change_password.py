"""Tests unitarios de ChangePassword."""

import pytest
import bcrypt
from unittest.mock import MagicMock

from tla.domain.use_cases.change_password import ChangePassword, WrongCurrentPasswordError
from tla.domain.use_cases.create_user import PasswordTooShortError


def _hashed(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt(rounds=4)).decode()


def _make_repo(current_pw: str = "oldpass1") -> MagicMock:
    repo = MagicMock()
    repo.get.return_value = MagicMock(id=1, password_hash=_hashed(current_pw))
    return repo


def test_change_password_success() -> None:
    repo = _make_repo("oldpass1")
    ChangePassword(repo=repo).execute("oldpass1", "newpass99")
    repo.update_password.assert_called_once()
    new_hash = repo.update_password.call_args.args[1]
    assert bcrypt.checkpw(b"newpass99", new_hash.encode())


def test_wrong_current_password_rejected() -> None:
    repo = _make_repo("oldpass1")
    with pytest.raises(WrongCurrentPasswordError):
        ChangePassword(repo=repo).execute("wrongold", "newpass99")
    repo.update_password.assert_not_called()


def test_new_password_too_short_rejected() -> None:
    repo = _make_repo("oldpass1")
    with pytest.raises(PasswordTooShortError):
        ChangePassword(repo=repo).execute("oldpass1", "short")
    repo.update_password.assert_not_called()
