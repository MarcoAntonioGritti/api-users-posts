from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apirestfull_curso.src.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    users: Mapped[list[User]] = relationship(back_populates="role")  # type: ignore
    # Uma role pode ter uma lista de users

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"
