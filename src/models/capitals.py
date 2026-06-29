import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.database import Base
from uuid import UUID, uuid4

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .countries import CountryModel

class CapitalModel(Base):
    __tablename__ = 'capitals'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String(50))

    country_id: Mapped[UUID] = mapped_column(sa.ForeignKey('countries.id', ondelete='CASCADE'), unique=True)
    country: Mapped['CountryModel'] = relationship(back_populates='capital')