from uuid import UUID
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session, get_read_session
from src.schemas.course import CourseSchemaCreate, CourseSchemaUpdate
from src.service.course_service import CourseService

router = APIRouter(prefix='/course')


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_course(data: CourseSchemaCreate, session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)
    return await course_service.create_course(data)


@router.get("/{course_id}")
async def read_course(course_id: UUID, session: AsyncSession = Depends(get_read_session)):
    course_service = CourseService(session)
    return await course_service.read_course(course_id)


@router.get("")
async def read_courses(offset: int, limit: int, session: AsyncSession = Depends(get_read_session)):
    course_service = CourseService(session)
    return await course_service.read_courses(offset, limit)


@router.put("/{course_id}")
async def update_course(course_id: UUID, data: CourseSchemaUpdate, session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)
    return await course_service.update_course(course_id, data)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: UUID, session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)
    await course_service.delete_course(course_id)
    return None