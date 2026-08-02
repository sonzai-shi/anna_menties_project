from uuid import UUID
from fastapi import APIRouter, status, HTTPException
from src.schemas.course import CourseSchemaCreate, CourseSchemaUpdate
import src.repositories.course_repository as cr

router = APIRouter()

@router.post("/course/", status_code=status.HTTP_201_CREATED)
async def post_course(data: CourseSchemaCreate):
    result = await cr.post_course(data)
    return {'result': result}

@router.get("/course/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id: UUID):
    result = await cr.get_course(course_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return {'result': result}

@router.put("/course/{course_id}", status_code=status.HTTP_200_OK)
async def put_course(course_id: UUID, data: CourseSchemaUpdate):
    result = await cr.put_course(course_id, data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return {'result': result}

@router.delete("/course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: UUID):
    result = await cr.delete_course(course_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return None