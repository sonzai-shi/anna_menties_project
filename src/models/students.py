import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from uuid import UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .courses import CourseModel


class StudentModel(Base):
    __tablename__ = 'students'

    name: Mapped[str] = mapped_column(sa.String(50))
    age: Mapped[int] = mapped_column(sa.Integer)
    dormitory: Mapped[str | None] = mapped_column(sa.String(150), nullable=True)
    citizenship: Mapped[str] = mapped_column(sa.String(150))

    course_id: Mapped[UUID] = mapped_column(sa.ForeignKey('courses.id', ondelete='CASCADE'))
    course: Mapped['CourseModel'] = relationship(back_populates='students')
