from typing import Annotated

from fastapi import HTTPException, status, Depends
import abc
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.config import Settings

settings = Settings()

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


class SessionCommit(AbstractSession):

    async def get_session(self) -> AsyncSession:
        async with SessionFactory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


class SessionRead(AbstractSession):

    async def get_session(self) -> AsyncSession:
        async with SessionFactory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


class ProjectServiceDependency:
    @classmethod
    def resolve_session(cls, session_type: str) -> AbstractSession:
        session_vendors = {
            'commit': SessionCommit,
            'read': SessionRead,
        }
        return session_vendors[session_type]()


get_session = ProjectServiceDependency.resolve_session('commit').get_session
get_read_session = ProjectServiceDependency.resolve_session('read').get_session