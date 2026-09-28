from uuid import UUID
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.mappers import course_mapper
from src.models.courses import CourseModel
from src.schemas.course import (
    CourseSchemaCreate,
    CourseSchemaResponse,
    CourseSchemaUpdate,
    CourseSchemaPagination,
)
from datetime import datetime
from src.repositories.repository import Repository
from src.exceptions.service_exception import ObjectNotFoundException, CursorException


class CourseService:
    def __init__(self, session: AsyncSession):
        self.course_repo = Repository(session)

    async def create_course(self, course_data: CourseSchemaCreate) -> CourseSchemaResponse:
        course = course_mapper.to_model(course_data)
        result = await self.course_repo.create(course)
        return CourseSchemaResponse.model_validate(result)

    async def read_course(self, course_id: UUID) -> CourseSchemaResponse:
        result = await self.find_course(course_id)
        return CourseSchemaResponse.model_validate(result)

    async def read_courses(
            self,
            limit: int,
            cursor_created_at: datetime | None,
            cursor_id: UUID | None,
    ) -> CourseSchemaPagination:
        if (cursor_created_at is None) != (cursor_id is None):
            raise CursorException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'You must provide both cursor_created_at and cursor_id.'
            )
        result = await self.course_repo.find_many(
            model=CourseModel,
            join_orm='students',
            limit=limit,
            cursor_created_at=cursor_created_at,
            cursor_id=cursor_id,
        )
        next_cursor_created_at = None
        next_cursor_id = None
        if result:
            last_course = result[-1]
            next_cursor_created_at = last_course.created_at
            next_cursor_id = last_course.id
        return course_mapper.to_pagination(
            courses=list(result),
            limit=limit,
            next_cursor_created_at=next_cursor_created_at,
            next_cursor_id=next_cursor_id,
        )

    async def update_course(self, course_id: UUID, data: CourseSchemaUpdate) -> CourseSchemaResponse:
        course = await self.find_course(course_id)
        await self.course_repo.update_one(CourseModel, course_id, 'students', data)
        return CourseSchemaResponse.model_validate(course)

    async def delete_course(self, course_id: UUID) -> str:
        result = await self.find_course(course_id)
        result.is_deleted = True
        for student in result.students:
            student.is_deleted = True
        return f'Course with ID: {course_id} has been removed.'

    async def find_course(self, course_id: UUID) -> CourseModel:
        result = await self.course_repo.find_one(CourseModel, course_id, 'students')
        if result is None:
            raise ObjectNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Course with ID: {course_id} not found.'
            )
        return result
