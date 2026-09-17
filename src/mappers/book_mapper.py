from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.schemas.book import (
    BookSchemaCreate,
    BookSchemaUpdate,
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


def to_paginated(books: list[BookModel], offset, limit) ->BookSchemaPagination:
    return BookSchemaPagination(
        items=[BookSchemaResponse.model_validate(book) for book in books],
        offset=offset,
        limit=limit,
    )


def update_book(book: BookModel, data: BookSchemaUpdate):
    update_data = data.model_dump(exclude_unset=True)
    authors_data = update_data.pop('authors', None)

    for field, value in update_data.items():
        setattr(book, field, value)

    if authors_data is not None:
        authors_id = {author.id: author for author in book.authors}

        for author_data in authors_data:
            author = authors_id.get(author_data['id'])
            for field, value in author_data.items():
                if field != 'id':
                    setattr(author, field, value)
