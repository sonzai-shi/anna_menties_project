from src.service.country_service import CountryService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db import get_session
from src.infrastructure.unit_of_work import UnitOfWork
from redis.asyncio import Redis
from src.dependencies.redis_dependencies import get_redis
from src.infrastructure.redis_cache import RedisCache
from src.repositories.repository import Repository


def get_uow(session: AsyncSession = Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session)


def get_country_service(
        session: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
        uow: UnitOfWork = Depends(get_uow),
) -> CountryService:
    country_redis = RedisCache(redis)
    country_repo = Repository(session)
    return CountryService(redis=country_redis, repository=country_repo, uow=uow)
