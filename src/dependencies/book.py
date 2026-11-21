from sqlalchemy.ext.asyncio import AsyncSession
from src.service.book_service import BookService
from src.infrastructure.db import get_session
from fastapi import Depends
from redis.asyncio import Redis
from src.dependencies.redis_dependencies import get_redis
from src.repositories.repository import Repository
from src.infrastructure.unit_of_work import UnitOfWork
from src.infrastructure.redis_cache import RedisCache


def get_uow(session: AsyncSession = Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session)


def get_book_service(
        session: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
        uow: UnitOfWork = Depends(get_uow),
) -> BookService:
    book_redis = RedisCache(redis)
    book_repo = Repository(session)
    return BookService(redis=book_redis, repository=book_repo, uow=uow)
