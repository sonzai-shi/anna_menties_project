from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.courses import CourseModel


async def create(session: AsyncSession, course: CourseModel):
    session.add(course)
    await session.flush()
    return course


async def find_course(session: AsyncSession, course_id: UUID):
    query = (
        select(CourseModel)
        .where(CourseModel.id == course_id)
        .where(CourseModel.is_deleted == False)
        .options(selectinload(CourseModel.students))
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()