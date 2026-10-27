from src.service.course_service import CourseService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session, get_read_session


def get_course_read_service(session: AsyncSession = Depends(get_read_session)) -> CourseService:
    return CourseService(session)


def get_course_write_service(session: AsyncSession = Depends(get_session)) -> CourseService:
    return CourseService(session)
