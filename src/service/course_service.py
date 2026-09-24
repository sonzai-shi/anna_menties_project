from uuid import UUID
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.mappers import course_mapper
from src.models.courses import CourseModel
from src.schemas.course import (
    CourseSchemaCreate,
    CourseSchemaResponse,
    CourseSchemaUpdate,
)
from src.repositories.repository import Repository
from src.exceptions.service_exception import ObjectNotFoundException


class CourseService:
    def __init__(self, session: AsyncSession):
        self.course_repo = Repository(session)

    async def create_course(self, course_data: CourseSchemaCreate):
        course = course_mapper.to_model(course_data)
        result = await self.course_repo.create(course)
        return CourseSchemaResponse.model_validate(result)

    async def read_course(self, course_id: UUID):
        result = await self.find_course(course_id)
        return CourseSchemaResponse.model_validate(result)

    async def read_courses(self, offset: int, limit: int):
        result = await self.course_repo.find_many(CourseModel, 'students', offset, limit)
        return course_mapper.to_pagination(courses=result, offset=offset, limit=limit)

    async def update_course(self, course_id: UUID, data: CourseSchemaUpdate):
        course = await self.find_course(course_id)
        await self.course_repo.update_one(CourseModel, course_id, 'students', data)
        return CourseSchemaResponse.model_validate(course)

    async def delete_course(self, course_id: UUID):
        result = await self.find_course(course_id)
        result.is_deleted = True
        for student in result.students:
            student.is_deleted = True
        return f'Course with ID: {course_id} has been removed.'

    async def find_course(self, course_id: UUID):
        result = await self.course_repo.find_one(CourseModel, course_id, 'students')
        if result is None:
            raise ObjectNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Course with ID: {course_id} not found.'
            )
        return result
