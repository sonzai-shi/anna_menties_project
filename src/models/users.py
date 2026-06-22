import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from src.models.database import Base
from uuid import UUID, uuid4

class UserModel(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(sa.String())
