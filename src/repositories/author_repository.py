from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.authors import AuthorModel


async def create(session: AsyncSession, author: AuthorModel):
    session.add(author)
    await session.flush()
    return author


async def find_authors_name(session: AsyncSession, name: str):
    query = (
        select(AuthorModel)
        .where(AuthorModel.name == name)
        .where(AuthorModel.is_deleted == False)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()