from __future__ import (  # Permite que os tipos anotados sejam avaliados em tempo de execução, corrigindo referências a classes ainda não definidas
    annotations,
)

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apirestfull_curso.src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(
        sa.ForeignKey("roles.id")
    )  # Vários users podem ter somente 1 role
    role: Mapped[Role] = relationship(back_populates="users")  # type: ignore
    posts: Mapped[list[Post]] = relationship("Post", back_populates="author")  # type: ignore

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"
        )
