from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.schemas.book import (
    BookSchemaCreate,
    BookSchemaPagination,
    BookSchemaResponse
)
from datetime import datetime
from uuid import UUID


def to_model(data: BookSchemaCreate) -> BookModel:
    book = BookModel(
        title=data.title,
        description=data.description,
        genre=data.genre,
        date_written=data.date_written,
    )

    authors = [
        AuthorModel(
            name=author.name,
            age=author.age,
            location=author.location,
            citizenship=author.citizenship,
        )
        for author in data.authors
    ]
    book.authors = authors
    return book


def to_paginated(
        books: list[BookModel],
        limit: int,
        next_cursor_created_at: datetime | None,
        next_cursor_id: UUID | None,
) -> BookSchemaPagination:
    return BookSchemaPagination(
        items=[BookSchemaResponse.model_validate(book) for book in books],
        limit=limit,
        next_cursor_created_at=next_cursor_created_at,
        next_cursor_id=next_cursor_id
    )
