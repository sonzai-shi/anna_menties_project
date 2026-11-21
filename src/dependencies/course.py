from sqlalchemy.ext.asyncio import AsyncSession
from src.service.course_service import CourseService
from src.infrastructure.db import get_session
from fastapi import Depends
from redis.asyncio import Redis
from src.dependencies.redis_dependencies import get_redis
from src.infrastructure.unit_of_work import UnitOfWork
from src.infrastructure.redis_cache import RedisCache
from src.repositories.repository import Repository


def get_uow(session: AsyncSession = Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session)


def get_course_service(
        session: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
        uow: UnitOfWork = Depends(get_uow),
) -> CourseService:
    course_redis = RedisCache(redis)
    course_repo = Repository(session)
    return CourseService(redis=course_redis, repository=course_repo, uow=uow)
