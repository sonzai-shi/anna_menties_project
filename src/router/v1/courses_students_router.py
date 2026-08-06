from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.schemas.course import CourseSchemaCreate, CourseSchemaUpdate
import src.service.course_service as course_service

router = APIRouter()

@router.post("/course/", status_code=status.HTTP_201_CREATED)
async def post_course(data: CourseSchemaCreate, session: AsyncSession = Depends(get_session)):
    result = await course_service.post_course(data, session)
    return {'result': result}

@router.get("/course/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await course_service.get_course(course_id, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return {'result': result}

@router.put("/course/{course_id}", status_code=status.HTTP_200_OK)
async def put_course(course_id: UUID, data: CourseSchemaUpdate, session: AsyncSession = Depends(get_session)):
    result = await course_service.put_course(course_id, data, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return {'result': result}

@router.delete("/course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await course_service.delete_course(course_id, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return None