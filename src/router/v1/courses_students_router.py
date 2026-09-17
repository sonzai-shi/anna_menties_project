from uuid import UUID
from fastapi import APIRouter, status, Depends
from src.schemas.course import CourseSchemaCreate, CourseSchemaUpdate
from src.service.course_service import CourseService
from src.dependencies.course import get_course_read_service, get_course_write_service

router = APIRouter(prefix='/course')


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_course(
        data: CourseSchemaCreate,
        course_service: CourseService = Depends(get_course_write_service),
):
    return await course_service.create_course(data)


@router.get("/{course_id}")
async def read_course(
        course_id: UUID,
        course_service: CourseService = Depends(get_course_read_service),
):
    return await course_service.read_course(course_id)


@router.get("")
async def read_courses(
        offset: int,
        limit: int,
        course_service: CourseService = Depends(get_course_read_service),
):
    return await course_service.read_courses(offset, limit)


@router.put("/{course_id}")
async def update_course(
        course_id: UUID,
        data: CourseSchemaUpdate,
        course_service: CourseService = Depends(get_course_write_service),
):
    return await course_service.update_course(course_id, data)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
        course_id: UUID,
        course_service: CourseService = Depends(get_course_write_service),
):
    await course_service.delete_course(course_id)
    return None
