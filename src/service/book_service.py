from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.mappers import book_mapper
from src.models.books import BookModel
from src.schemas.book import (
    BookSchemaCreate,
    BookSchemaResponse,
    BookSchemaUpdate,
)
from src.repositories.repository import Repository


class BookService:
    def __init__(self, session: AsyncSession):
        self.book_repo = Repository(session)


    async def create_books(self, data: BookSchemaCreate):
        book = book_mapper.to_model(data)
        result = await self.book_repo.create(book)
        return BookSchemaResponse.model_validate(result)


    async def read_book(self, book_id: UUID):
        result = await self.find_book(book_id)
        return BookSchemaResponse.model_validate(result)


    async def read_books(self, offset: int, limit: int):
        result = await self.book_repo.find_many(BookModel, 'authors', offset, limit)
        return book_mapper.to_paginated(books=result, offset=offset, limit=limit)


    async def update_book(self, book_id: UUID, book_data: BookSchemaUpdate):
        book = await self.find_book(book_id)
        book_mapper.update_book(book, book_data)
        return BookSchemaResponse.model_validate(book)


    async def delete_book(self, book_id: UUID):
        result = await self.find_book(book_id)
        result.is_deleted = True
        return 'The book has been removed.'


    async def find_book(self, book_id: UUID):
        result = await self.book_repo.find_one(BookModel, book_id, 'authors')
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Book not found.'
            )
        return result