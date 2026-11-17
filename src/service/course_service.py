from uuid import UUID
from fastapi import status
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
from src.infrastructure.unit_of_work import UnitOfWork
from src.infrastructure.redis_cache import RedisCache


class CourseService:
    MODEL_NAME = 'course'
    RELATION_NAME = 'students'

    def __init__(
            self,
            redis: RedisCache,
            repository: Repository,
            uow: UnitOfWork,
    ) -> None:
        self.course_repo = repository
        self.uow = uow
        self.course_redis = redis

    async def create_course(self, course_data: CourseSchemaCreate) -> CourseSchemaResponse:
        async with self.uow:
            course = course_mapper.to_model(course_data)
            result = await self.course_repo.create(course)
            schema_response = CourseSchemaResponse.model_validate(result)
        return schema_response

    async def read_course(self, course_id: UUID) -> CourseSchemaResponse:
        result_cache = await self.course_redis.get(model_name=self.MODEL_NAME, key=course_id)
        if result_cache:
            return CourseSchemaResponse.model_validate_json(result_cache)
        result = await self.find_course(course_id)
        schema_response = CourseSchemaResponse.model_validate(result)
        await self.course_redis.set(model_name=self.MODEL_NAME, key=course_id, value=schema_response.model_dump_json())
        return schema_response

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
            join_orm=self.RELATION_NAME,
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

        course_cache_data = {
            course.id:
                CourseSchemaResponse
                .model_validate(course)
                .model_dump_json()
            for course in result
        }
        await self.course_redis.sets(
            model_name=self.MODEL_NAME,
            data=course_cache_data,
        )

        return course_mapper.to_pagination(
            courses=list(result),
            limit=limit,
            next_cursor_created_at=next_cursor_created_at,
            next_cursor_id=next_cursor_id,
        )

    async def update_course(self, course_id: UUID, data: CourseSchemaUpdate) -> CourseSchemaResponse:
        async with self.uow:
            course = await self.course_repo.find_one(CourseModel, course_id, self.RELATION_NAME)
            if course is None:
                self.raise_course_not_found(course_id)
            await self.course_repo.update_one(CourseModel, course_id, self.RELATION_NAME, data)
            schema_response = CourseSchemaResponse.model_validate(course)
        await self.course_redis.set(model_name=self.MODEL_NAME, key=course_id, value=schema_response.model_dump_json())
        return schema_response

    async def delete_course(self, course_id: UUID) -> str:
        async with self.uow:
            result = await self.course_repo.find_one(CourseModel, course_id, self.RELATION_NAME)
            if result is None:
                self.raise_course_not_found(course_id)
            result.is_deleted = True
            for student in result.students:
                student.is_deleted = True
        return f'Course with ID: {course_id} has been removed.'

    async def find_course(self, course_id: UUID) -> CourseModel:
        result = await self.course_repo.find_one(CourseModel, course_id, self.RELATION_NAME)
        if result is None:
            self.raise_course_not_found(course_id)
        return result

    def raise_course_not_found(self, course_id: UUID):
        raise ObjectNotFoundException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Course with ID: {course_id} not found.'
        )
