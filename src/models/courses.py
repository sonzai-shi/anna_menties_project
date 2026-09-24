import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .students import StudentModel


class CourseModel(Base):
    __tablename__ = 'courses'

    title: Mapped[str] = mapped_column(sa.String(150))
    description: Mapped[str] = mapped_column(sa.String(1000))
    mentor: Mapped[str] = mapped_column(sa.String(150))
    teaching_hours: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)

    students: Mapped[list['StudentModel']] = relationship(back_populates="course", cascade="all, delete-orphan")
