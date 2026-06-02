"""Implementación SQLModel de UserRepository."""

from __future__ import annotations

from typing import Optional

from sqlmodel import Session, select

from tla.adapters.db.models import User
from tla.domain.ports.user_repository import UserRepository


class SQLUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def get(self) -> Optional[User]:
        return self._session.exec(select(User)).first()

    def exists(self) -> bool:
        return self.get() is not None

    def update_password(self, user_id: int, new_hash: str) -> None:
        user = self._session.get(User, user_id)
        if user:
            user.password_hash = new_hash
            self._session.add(user)
            self._session.commit()
