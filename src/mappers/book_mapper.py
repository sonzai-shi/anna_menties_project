from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.schemas.book import (
    BookSchemaCreate,
    BookSchemaPagination,
    BookSchemaResponse
)


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


def to_paginated(books: list[BookModel], offset, limit) -> BookSchemaPagination:
    return BookSchemaPagination(
        items=[BookSchemaResponse.model_validate(book) for book in books],
        offset=offset,
        limit=limit,
    )
