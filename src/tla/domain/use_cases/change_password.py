"""Use case: cambiar la contraseña."""

from __future__ import annotations

from dataclasses import dataclass

import bcrypt

from tla.domain.exceptions import TLAError
from tla.domain.ports.user_repository import UserRepository
from tla.domain.use_cases.create_user import PasswordTooShortError, _BCRYPT_COST, _MIN_PASSWORD_LENGTH


class WrongCurrentPasswordError(TLAError):
    pass


@dataclass
class ChangePassword:
    repo: UserRepository

    def execute(self, current_password: str, new_password: str) -> None:
        user = self.repo.get()
        if user is None:
            raise TLAError("No hay ningún usuario registrado.")

        if not bcrypt.checkpw(current_password.encode(), user.password_hash.encode()):
            raise WrongCurrentPasswordError("La contraseña actual es incorrecta.")

        if len(new_password) < _MIN_PASSWORD_LENGTH:
            raise PasswordTooShortError(
                f"La nueva contraseña debe tener al menos {_MIN_PASSWORD_LENGTH} caracteres."
            )

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt(rounds=_BCRYPT_COST)).decode()
        self.repo.update_password(user.id, new_hash)  # type: ignore[arg-type]
