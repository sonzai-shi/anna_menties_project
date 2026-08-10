from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.schemas.book import BookSchemaCreate, BookSchemaResponse, BookSchemaUpdate, BookSchemaPagination
import src.repositories.book_repository as book_repo
import src.repositories.author_repository as author_repo


async def post_books(data: BookSchemaCreate, session: AsyncSession):
    book = BookModel(
        title=data.title,
        description=data.description,
        genre=data.genre,
        date_written=data.date_written,
    )

    authors = []
    for item in data.authors:
        author = await author_repo.find_authors_name(session, item.name)
        if author is None:
            author = AuthorModel(
                name=item.name,
                age=item.age,
                location=item.location,
                citizenship=item.citizenship,
            )
            author = await author_repo.create(session, author)
        authors.append(author)

    book.authors = authors
    result = await book_repo.create(session, book)
    return BookSchemaResponse.model_validate(result)


async def get_book(book_id: UUID, session: AsyncSession):
    result = await book_repo.find_book(session, book_id)
    if result is None:
        return None
    return BookSchemaResponse.model_validate(result)


async def get_books(offset: int, limit: int, session: AsyncSession):
    result = await book_repo.find_books(session, offset, limit)
    if result is None:
        return None

    return BookSchemaPagination(
        items=[BookSchemaResponse.model_validate(book) for book in result],
        offset=offset,
        limit=limit,
    )


async def put_book(book_id: UUID, book_data: BookSchemaUpdate, session: AsyncSession):
    book = await book_repo.find_book(session, book_id)
    if book is None:
        return None

    if book_data.title is not None:
        book.title = book_data.title
    if book_data.description is not None:
        book.description = book_data.description
    if book_data.genre is not None:
        book.genre = book_data.genre
    if book_data.date_written is not None:
        book.date_written = book_data.date_written

    if book_data.authors is not None:
        authors_id = {a.id: a for a in book.authors}

        for author_data in book_data.authors:
            author = authors_id.get(author_data.id)
            if author is None:
                continue
            if author_data.name is not None:
                author.name = author_data.name
            if author_data.age is not None:
                author.age = author_data.age
            if author_data.location is not None:
                author.location = author_data.location
            if author_data.citizenship is not None:
                author.citizenship = author_data.citizenship
    return BookSchemaResponse.model_validate(book)


async def delete_book(book_id: UUID, session: AsyncSession):
    result = await book_repo.find_book(session, book_id)
    if result is None:
        return None
    result.is_deleted = True
    return True