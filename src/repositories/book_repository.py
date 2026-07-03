from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.db import get_session
from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.schemas.book_schema import BookSchemaCreate, BookSchemaUpdate


async def post_books(data: BookSchemaCreate):
    async with get_session() as session:
        db_books = BookModel(title=data.title)

        authors = []
        for item in data.authors:
            author = await _find_authors_name(session, item.name)
            if author is None:
                author = AuthorModel(name=item.name)
            authors.append(author)

        db_books.authors = authors
        session.add(db_books)
        await session.flush()

        return {
            'id': db_books.id,
            'title': db_books.title,
            'authors': [
                {'id': book.id, 'name': book.name}
                for book in db_books.authors
            ],
        }

async def _find_authors_name(session, name: str):
    query = select(AuthorModel).where(AuthorModel.name == name)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_book(book_id: UUID):
    async with get_session() as session:
        db_books = _find_book(session, book_id)
        if db_books is None:
            return None
        return {
            'id': db_books.id,
            'title': db_books.title,
            'authors': [
                {'id': book.id, 'name': book.name}
                for book in db_books.authors
            ],
        }


async def put_book(book_id: UUID, book_data: BookSchemaUpdate):
    async with get_session() as session:
        db_books = _find_book(session, book_id)
        if db_books is None:
            return None
        db_books.title = book_data.title
        id_authors = {s.id: s for s in db_books.authors}

        for author_data in book_data.authors:
            author = id_authors.get(author_data.id)
            if author is None:
                continue
            author.name = author_data.name

        await session.flush()

        return {
            'id': db_books.id,
            'title': db_books.title,
            'students': [
                {'id': author.id, 'name': author.name}
                for author in db_books.authors
            ],
        }


async def delete_book(book_id: UUID):
    async with get_session() as session:
        book = await _find_book(session, book_id)
        if book is None:
            return None
        book.is_deleted = True
        return True

async def _find_book(session: AsyncSession, book_id: UUID):
    query = (
        select(BookModel)
        .where(BookModel.id == book_id)
        .where(BookModel.is_deleted == False)
        .options(selectinload(BookModel.authors))
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()