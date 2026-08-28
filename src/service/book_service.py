from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.schemas.book import BookSchemaCreate, BookSchemaResponse, BookSchemaUpdate, BookSchemaPagination
from src.repositories.repository import Repository
class BookService:
    def __init__(self, session: AsyncSession):
        self.book_repo = Repository(session)


    async def create_books(self, data: BookSchemaCreate):
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
        result = await self.book_repo.create(book)
        return BookSchemaResponse.model_validate(result)


    async def read_book(self, book_id: UUID):
        result = await self.book_repo.find_one(BookModel, book_id, 'authors')
        if result is None:
            return None
        return BookSchemaResponse.model_validate(result)


    async def read_books(self, offset: int, limit: int):
        result = await self.book_repo.find_many(BookModel, 'authors', offset, limit)
        if result is None:
            return None

        return BookSchemaPagination(
            items=[BookSchemaResponse.model_validate(book) for book in result],
            offset=offset,
            limit=limit,
        )


    async def update_book(self, book_id: UUID, book_data: BookSchemaUpdate):
        book = await self.book_repo.find_one(BookModel, book_id, 'authors')
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


    async def delete_book(self, book_id: UUID):
        result = await self.book_repo.find_one(BookModel, book_id, 'authors')
        if result is None:
            return None
        result.is_deleted = True
        return True