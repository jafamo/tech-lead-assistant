"""Use case: crear la cuenta de usuario."""

from __future__ import annotations

from dataclasses import dataclass

import bcrypt

from tla.adapters.db.models import User
from tla.domain.exceptions import TLAError
from tla.domain.ports.user_repository import UserRepository

_MIN_PASSWORD_LENGTH = 8
_BCRYPT_COST = 12


class UserAlreadyExistsError(TLAError):
    pass


class PasswordTooShortError(TLAError):
    pass


@dataclass
class CreateUser:
    repo: UserRepository

    def execute(self, username: str, password: str) -> User:
        if len(password) < _MIN_PASSWORD_LENGTH:
            raise PasswordTooShortError(
                f"La contraseña debe tener al menos {_MIN_PASSWORD_LENGTH} caracteres."
            )
        if self.repo.exists():
            raise UserAlreadyExistsError("Ya existe una cuenta de usuario.")

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=_BCRYPT_COST)).decode()
        return self.repo.create(username=username, password_hash=pw_hash)
