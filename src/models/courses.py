import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from uuid import UUID, uuid4

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .students import StudentModel


class CourseModel(Base):
    __tablename__ = 'courses'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(sa.String(150))

    students: Mapped[list['StudentModel']] = relationship(back_populates="course", cascade="all, delete-orphan")
