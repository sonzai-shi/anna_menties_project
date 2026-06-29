import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.database import Base
from uuid import UUID, uuid4

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .capitals import CapitalModel

class CountryModel(Base):
    __tablename__ = 'countries'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String(50))

    capital: Mapped['CapitalModel'] = relationship(back_populates='country', uselist=False, cascade='all, delete-orphan')
