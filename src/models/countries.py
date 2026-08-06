import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .capitals import CapitalModel


class CountryModel(Base):
    __tablename__ = 'countries'

    name: Mapped[str] = mapped_column(sa.String(50))
    president: Mapped[str] = mapped_column(sa.String(100))
    population: Mapped[int] = mapped_column(sa.BigInteger)
    currency: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)

    capital: Mapped['CapitalModel'] = relationship(back_populates='country', uselist=False, cascade='all, delete-orphan')
