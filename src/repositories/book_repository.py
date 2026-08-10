from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.books import BookModel


async def create(session: AsyncSession, book: BookModel):
    session.add(book)
    await session.flush()
    return book


async def find_book(session: AsyncSession, book_id: UUID):
    query = (
        select(BookModel)
        .where(BookModel.id == book_id)
        .where(BookModel.is_deleted == False)
        .options(selectinload(BookModel.authors))
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def find_books(session: AsyncSession, offset: int, limit: int):
    query = (
        select(BookModel)
        .where(BookModel.is_deleted == False)
        .options(selectinload(BookModel.authors))
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(query)
    return result.scalars().all()