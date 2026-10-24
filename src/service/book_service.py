from uuid import UUID
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.mappers import book_mapper
from src.models.books import BookModel
from src.schemas.book import (
    BookSchemaCreate,
    BookSchemaResponse,
    BookSchemaUpdate,
    BookSchemaPagination,
)
from redis.asyncio import Redis
from datetime import datetime
from src.repositories.repository import Repository
from src.exceptions.service_exception import ObjectNotFoundException, CursorException
from src.cache.redis_cache import RedisCache
from src.unit_of_work import UnitOfWork


class BookService:
    def __init__(
            self,
            redis: Redis,
            session: AsyncSession | None = None,
            uow: UnitOfWork | None = None,
    ) -> None:
        if session is not None:
            self.book_repo = Repository(session)
            self.uow = None
        else:
            self.book_repo = None
            self.uow = uow
        self.book_redis = RedisCache(redis)

    async def create_books(self, data: BookSchemaCreate) -> BookSchemaResponse:
        async with self.uow as uow:
            local_book_repo = Repository(uow.session)
            book = book_mapper.to_model(data)
            result = await local_book_repo.create(book)
            schema_response = BookSchemaResponse.model_validate(result)
        return schema_response

    async def read_book(self, book_id: UUID) -> BookSchemaResponse:
        result_cache = await self.book_redis.get(model_name='book', key=book_id)
        if result_cache:
            return BookSchemaResponse.model_validate_json(result_cache)
        result = await self.find_book(book_id)
        schema_response = BookSchemaResponse.model_validate(result)
        await self.book_redis.set(model_name='book', key=book_id, value=schema_response.model_dump_json())
        return schema_response

    async def read_books(self, limit: int, cursor_created_at: datetime | None,
                         cursor_id: UUID | None) -> BookSchemaPagination:
        if (cursor_created_at is None) != (cursor_id is None):
            raise CursorException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'You must provide both cursor_created_at and cursor_id.'
            )
        result = await self.book_repo.find_many(
            model=BookModel,
            join_orm='authors',
            limit=limit,
            cursor_created_at=cursor_created_at,
            cursor_id=cursor_id,
        )
        next_cursor_created_at = None
        next_cursor_id = None

        if result:
            last_book = result[-1]
            next_cursor_created_at = last_book.created_at
            next_cursor_id = last_book.id

        books_cache_data = {book.id: BookSchemaResponse.model_validate(book).model_dump_json() for book in result}
        await self.book_redis.sets(
            model_name='book',
            data=books_cache_data,
        )

        return book_mapper.to_paginated(
            books=result,
            limit=limit,
            next_cursor_created_at=next_cursor_created_at,
            next_cursor_id=next_cursor_id,
        )

    async def update_book(self, book_id: UUID, book_data: BookSchemaUpdate) -> BookSchemaResponse:
        async with self.uow as uow:
            local_book_repo = Repository(uow.session)
            book = await local_book_repo.find_one(BookModel, book_id, 'authors')
            if book is None:
                self.raise_book_not_found(book_id)
            await local_book_repo.update_one(BookModel, book_id, 'authors', book_data)
            schema_response = BookSchemaResponse.model_validate(book)
        await self.book_redis.set(model_name='book', key=book_id, value=schema_response.model_dump_json())
        return schema_response

    async def delete_book(self, book_id: UUID) -> str:
        async with self.uow as uow:
            local_book_repo = Repository(uow.session)
            result = await local_book_repo.find_one(BookModel, book_id, 'authors')
            if result is None:
                self.raise_book_not_found(book_id)
            result.is_deleted = True
        return f'Book with ID: {book_id} has been deleted.'

    async def find_book(self, book_id: UUID) -> BookModel:
        result = await self.book_repo.find_one(BookModel, book_id, 'authors')
        if result is None:
            self.raise_book_not_found(book_id)
        return result

    def raise_book_not_found(self, book_id: UUID):
        raise ObjectNotFoundException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Book with ID: {book_id} not found.'
        )
