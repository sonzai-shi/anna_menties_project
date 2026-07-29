import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from uuid import UUID, uuid4
from src.models.books import book_author_table

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .books import BookModel


class AuthorModel(Base):
    __tablename__ = 'authors'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String(50))

    age: Mapped[int] = mapped_column(sa.Integer)
    location: Mapped[str| None] = mapped_column(sa.String(150), nullable=True)
    citizenship: Mapped[str | None] = mapped_column(sa.String(150), nullable=True)

    books: Mapped[list['BookModel']] = relationship(secondary=book_author_table, back_populates='authors')