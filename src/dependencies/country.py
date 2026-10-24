from src.service.country_service import CountryService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_read_session
from src.unit_of_work import UnitOfWork
from src.db import SessionFactory
from redis.asyncio import Redis
from src.cache.redis_client import get_redis


def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionFactory)


def get_country_read_service(
        session: AsyncSession = Depends(get_read_session),
        redis: Redis = Depends(get_redis),
) -> CountryService:
    return CountryService(redis, session=session, uow=None)


def get_country_write_service(
        redis: Redis = Depends(get_redis),
        uow: UnitOfWork = Depends(get_uow),
) -> CountryService:
    return CountryService(redis, session=None, uow=uow)
