import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from uuid import UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .countries import CountryModel


class CapitalModel(Base):
    __tablename__ = 'capitals'

    name: Mapped[str] = mapped_column(sa.String(50))
    mayor: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    population: Mapped[int] = mapped_column(sa.BigInteger)

    country_id: Mapped[UUID] = mapped_column(sa.ForeignKey('countries.id', ondelete='CASCADE'), unique=True)
    country: Mapped['CountryModel'] = relationship(back_populates='capital')