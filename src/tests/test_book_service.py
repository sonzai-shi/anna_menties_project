import uuid
from datetime import date
import pytest

from src.exceptions.service_exception import ObjectNotFoundException
from src.schemas.book import BookSchemaResponse, BookSchemaUpdate
from src.service.book_service import BookService
from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.unit_of_work import UnitOfWork


@pytest.mark.asyncio
async def test_empty_cache(db_session, redis_client):
    author1 = AuthorModel(
        name='Fifiv',
        age=25,
        location='Mock',
        citizenship='Da',
    )
    author1.id = uuid.uuid4()
    author2 = AuthorModel(
        name='Fafav',
        age=28,
        location='Fack',
        citizenship='Net',
    )
    author2.id = uuid.uuid4()
    book = BookModel(
        title='Mima',
        description='test',
        genre=['horror', 'rom', 'fan'],
        date_written=date(2026, 9, 16),
        authors=[author1, author2],
    )
    book.id = uuid.uuid4()
    db_session.add(book)
    await db_session.commit()
    result = await redis_client.get(name=f'book:{book.id}')
    assert result is None

    service = BookService(session=db_session, redis=redis_client, uow=None)
    schema_response = await service.read_book(book.id)

    assert schema_response.id == book.id
    assert schema_response.title == 'Mima'
    assert schema_response.description == 'test'
    assert schema_response.genre == ['horror', 'rom', 'fan']
    assert schema_response.date_written == date(2026, 9, 16)
    ids_response = [author.id for author in schema_response.authors]
    assert author1.id in ids_response
    assert author2.id in ids_response
    assert len(ids_response) == 2

    book_cache = await redis_client.get(name=f'book:{book.id}')
    assert book_cache is not None
    book_cache = BookSchemaResponse.model_validate_json(book_cache)

    assert book_cache.id == book.id
    assert book_cache.title == 'Mima'
    assert book_cache.description == 'test'
    assert book_cache.genre == ['horror', 'rom', 'fan']
    assert book_cache.date_written == date(2026, 9, 16)
    ids_response = [author.id for author in book_cache.authors]
    assert author1.id in ids_response
    assert author2.id in ids_response
    assert len(ids_response) == 2
    book_ttl = await redis_client.ttl(name=f'book:{book.id}')
    assert 0 < book_ttl <= 3600


@pytest.mark.asyncio
async def test_book_in_cache(db_session, redis_client):
    author1 = AuthorModel(
        name='Dade',
        age=12,
        location='Wert',
        citizenship='Saert',
    )
    author1.id = uuid.uuid4()
    author2 = AuthorModel(
        name='Ferta',
        age=45,
        location='Xaw',
        citizenship='Gasr',
    )
    author2.id = uuid.uuid4()
    book = BookModel(
        title='Car',
        description='dasertiom',
        genre=['wet', 'aswq', 'Qerop'],
        date_written=date(2024, 12, 24),
        authors=[author1, author2],
    )
    book.id = uuid.uuid4()
    schema_response = BookSchemaResponse.model_validate(book)
    await redis_client.set(name=f'book:{book.id}', value=schema_response.model_dump_json(), ex=3600)

    service = BookService(session=db_session, redis=redis_client, uow=None)
    schema_response = await service.read_book(book.id)

    assert schema_response is not None
    assert schema_response.id == book.id
    assert schema_response.title == 'Car'
    assert schema_response.description == 'dasertiom'
    assert schema_response.genre == ['wet', 'aswq', 'Qerop']
    assert schema_response.date_written == date(2024, 12, 24)
    ids_response = [author.id for author in schema_response.authors]
    assert author1.id in ids_response
    assert author2.id in ids_response
    assert len(ids_response) == 2
    book_ttl = await redis_client.ttl(name=f'book:{book.id}')
    assert 0 < book_ttl <= 3600


@pytest.mark.asyncio
async def test_book_not_found(db_session, redis_client):
    book_id = uuid.uuid4()
    service = BookService(session=db_session, redis=redis_client, uow=None)
    with pytest.raises(ObjectNotFoundException):
        await service.read_book(book_id)
    result = await redis_client.get(name=f'book:{book_id}')
    assert result is None


@pytest.mark.asyncio
async def test_many_books(db_session, redis_client):
    author1 = AuthorModel(
        name='Fifiv',
        age=25,
        location='Mock',
        citizenship='Da',
    )
    author1.id = uuid.uuid4()
    author2 = AuthorModel(
        name='Fafav',
        age=28,
        location='Fack',
        citizenship='Net',
    )
    author2.id = uuid.uuid4()
    book1 = BookModel(
        title='Mima',
        description='test',
        genre=['horror', 'rom', 'fan'],
        date_written=date(2026, 9, 16),
        authors=[author1, author2],
    )
    book1.id = uuid.uuid4()

    author3 = AuthorModel(
        name='Dade',
        age=12,
        location='Wert',
        citizenship='Saert',
    )
    author3.id = uuid.uuid4()
    author4 = AuthorModel(
        name='Ferta',
        age=45,
        location='Xaw',
        citizenship='Gasr',
    )
    author4.id = uuid.uuid4()
    book2 = BookModel(
        title='Car',
        description='dasertiom',
        genre=['wet', 'aswq', 'Qerop'],
        date_written=date(2024, 12, 24),
        authors=[author3, author4],
    )
    book2.id = uuid.uuid4()
    db_session.add(book1)
    db_session.add(book2)
    await db_session.commit()
    service = BookService(session=db_session, redis=redis_client, uow=None)

    result_schema_response = await service.read_books(limit=2, cursor_created_at=None, cursor_id=None)
    assert result_schema_response is not None
    assert len(result_schema_response.items) == 2

    ids_response = [book.id for book in result_schema_response.items]
    assert book1.id in ids_response
    assert book2.id in ids_response

    for book_response in result_schema_response.items:
        book_cache = await redis_client.get(name=f'book:{book_response.id}')
        assert book_cache is not None
        book_cache = BookSchemaResponse.model_validate_json(book_cache)
        assert book_response.id == book_cache.id
        assert book_response.title == book_cache.title
        assert book_response.description == book_cache.description
        assert book_response.genre == book_cache.genre
        assert book_response.date_written == book_cache.date_written
        assert book_response.authors == book_cache.authors
        ttl_id = await redis_client.ttl(name=f'book:{book_response.id}')
        assert 0 < ttl_id <= 3600


@pytest.mark.asyncio
async def test_many_books_not_found(db_session, redis_client):
    service = BookService(session=db_session, redis=redis_client, uow=None)
    result_schema_response = await service.read_books(limit=2, cursor_created_at=None, cursor_id=None)
    assert len(result_schema_response.items) == 0
    assert result_schema_response.next_cursor_id is None
    assert result_schema_response.next_cursor_created_at is None
    assert result_schema_response.limit == 2

    id_list = []
    async for key in redis_client.scan_iter(match='book:*'):
        id_list.append(key)
    assert len(id_list) == 0


@pytest.mark.asyncio
async def test_update_books(db_session, db_session_factory, redis_client):
    author1 = AuthorModel(
        name='Fifiv',
        age=25,
        location='Mock',
        citizenship='Da',
    )
    author1.id = uuid.uuid4()
    author2 = AuthorModel(
        name='Fafav',
        age=28,
        location='Fack',
        citizenship='Net',
    )
    author2.id = uuid.uuid4()
    book = BookModel(
        title='Mima',
        description='test',
        genre=['horror', 'rom', 'fan'],
        date_written=date(2026, 9, 16),
        authors=[author1, author2],
    )
    book.id = uuid.uuid4()
    db_session.add(book)
    await db_session.commit()

    uow = UnitOfWork(session_factory=db_session_factory)
    service = BookService(session=None, redis=redis_client, uow=uow)
    schema_response = BookSchemaResponse.model_validate(book)
    await redis_client.set(name=f'book:{book.id}', value=schema_response.model_dump_json(), ex=3600)
    book_update = BookSchemaUpdate(title='Kizil', genre=['Darest', 'rom', 'fan', 'Frsanc'])
    result_update = await service.update_book(book.id, book_update)

    assert result_update is not None
    assert result_update.id == book.id
    assert result_update.title == 'Kizil'
    assert result_update.description == 'test'
    assert result_update.genre == ['Darest', 'rom', 'fan', 'Frsanc']
    assert result_update.date_written == date(2026, 9, 16)
    ids_result_update = [author.id for author in result_update.authors]
    assert len(ids_result_update) == 2
    assert author1.id in ids_result_update
    assert author2.id in ids_result_update

    book_update_cache = await redis_client.get(name=f'book:{book.id}')
    assert book_update_cache is not None
    book_update_cache = BookSchemaResponse.model_validate_json(book_update_cache)
    assert book_update_cache is not None
    assert book_update_cache.id == book.id
    assert book_update_cache.title == 'Kizil'
    assert book_update_cache.description == 'test'
    assert book_update_cache.genre == ['Darest', 'rom', 'fan', 'Frsanc']
    assert book_update_cache.date_written == date(2026, 9, 16)
    ids_response = [author.id for author in book_update_cache.authors]
    assert len(ids_response) == 2
    assert author1.id in ids_response
    assert author2.id in ids_response
    ttl_id = await redis_client.ttl(name=f'book:{book.id}')
    assert 0 < ttl_id <= 3600


@pytest.mark.asyncio
async def test_update_not_found_book(db_session, db_session_factory, redis_client):
    book_id = uuid.uuid4()
    uow = UnitOfWork(session_factory=db_session_factory)
    service = BookService(session=None, redis=redis_client, uow=uow)
    with pytest.raises(ObjectNotFoundException):
        await service.update_book(book_id, BookSchemaUpdate(title='Kizil'))
    result = await redis_client.get(name=f'book:{book_id}')
    assert result is None
