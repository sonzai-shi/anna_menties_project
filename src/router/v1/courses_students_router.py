from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.schemas.course import CourseSchemaCreate, CourseSchemaUpdate
from src.service.course_service import CourseService

router = APIRouter(prefix='/course')


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_course(data: CourseSchemaCreate, session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)
    result = await course_service.create_course(data)
    return {'result': result}


@router.get("/{course_id}")
async def get_course(course_id: UUID, session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)
    result = await course_service.read_course(course_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return {'result': result}


@router.get("")
async def get_courses(offset: int, limit: int, session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)
    result = await course_service.read_courses(offset, limit)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return {'result': result}


@router.put("/{course_id}")
async def put_course(course_id: UUID, data: CourseSchemaUpdate, session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)
    result = await course_service.update_course(course_id, data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return {'result': result}


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: UUID, session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)
    result = await course_service.delete_course(course_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return None