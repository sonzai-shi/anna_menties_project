import abc
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from src.config import settings

engine: AsyncEngine = create_async_engine(
    str(settings.postgres_url),
    pool_pre_ping=True,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class AbstractSession(abc.ABC):

    @abc.abstractmethod
    def get_session(self):
        pass


class SessionProvider(AbstractSession):

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with SessionFactory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


get_session = SessionProvider().get_session
