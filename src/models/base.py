from datetime import datetime, timezone
from uuid import UUID, uuid4
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeMeta, declarative_base, Mapped, mapped_column

metadata = sa.MetaData()


class BaseServiceModel:
    """Базовый класс для таблиц сервиса."""
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )
    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        server_default=sa.false(),
    )

    @classmethod
    def on_conflict_constraint(cls) -> tuple | None:
        return None


Base: DeclarativeMeta = declarative_base(metadata=metadata, cls=BaseServiceModel)

