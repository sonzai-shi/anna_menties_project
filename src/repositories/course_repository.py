from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.courses import CourseModel


class CourseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, course: CourseModel):
        self.session.add(course)
        await self.session.flush()
        return course


    async def find_course(self, course_id: UUID):
        query = (
            select(CourseModel)
            .where(CourseModel.id == course_id)
            .where(CourseModel.is_deleted == False)
            .options(selectinload(CourseModel.students))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def find_courses(self, offset: int, limit: int):
        query = (
            select(CourseModel)
            .where(CourseModel.is_deleted == False)
            .options(selectinload(CourseModel.students))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()


