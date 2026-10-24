from sqlalchemy.ext.asyncio import AsyncSession
from src.service.course_service import CourseService
from src.db import get_read_session
from fastapi import Depends
from redis.asyncio import Redis
from src.cache.redis_client import get_redis
from src.unit_of_work import UnitOfWork
from src.db import SessionFactory


def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionFactory)


def get_course_read_service(
        session: AsyncSession = Depends(get_read_session),
        redis: Redis = Depends(get_redis),
) -> CourseService:
    return CourseService(redis, session=session, uow=None)


def get_course_write_service(
        redis: Redis = Depends(get_redis),
        uow: UnitOfWork = Depends(get_uow),
) -> CourseService:
    return CourseService(redis, session=None, uow=uow)
