import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class UserModel(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(sa.String())
