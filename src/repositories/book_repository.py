from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.books import BookModel


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, book: BookModel):
        self.session.add(book)
        await self.session.flush()
        return book


    async def find_book(self, book_id: UUID, authors):
        query = (
            select(BookModel)
            .where(BookModel.id == book_id)
            .where(BookModel.is_deleted == False)
            .options(selectinload(BookModel.authors))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def find_books(self, offset: int, limit: int):
        query = (
            select(BookModel)
            .where(BookModel.is_deleted == False)
            .options(selectinload(BookModel.authors))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()