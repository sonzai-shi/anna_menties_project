from datetime import date
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from uuid import UUID, uuid4

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .authors import AuthorModel


book_author_table = sa.Table(
    'book_author',
    Base.metadata,
    sa.Column('book_id', sa.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    sa.Column('author_id', sa.ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True),
)


class BookModel(Base):
    __tablename__ = 'books'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(sa.String(150))

    description: Mapped[str] = mapped_column(sa.String(1000))
    genre: Mapped[list[str] | None] = mapped_column(sa.ARRAY(sa.String(150)), nullable=True)
    date_written: Mapped[date] = mapped_column(sa.Date)

    authors: Mapped[list['AuthorModel']] = relationship(secondary=book_author_table, back_populates='books')
