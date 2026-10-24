import uuid
from datetime import date
import pytest_asyncio
from testcontainers.redis import RedisContainer
from redis.asyncio import Redis
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.db import get_read_session
from src.application import get_app
from src.cache.redis_client import get_redis
from src.unit_of_work import UnitOfWork
from src.dependencies.book import get_uow as get_book_uow
from src.dependencies.course import get_uow as get_course_uow
from src.dependencies.country import get_uow as get_country_uow
import httpx
from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.models.students import StudentModel
from src.models.courses import CourseModel
from src.models.capitals import CapitalModel
from src.models.countries import CountryModel
from src.schemas.book import BookSchemaResponse
from src.schemas.course import CourseSchemaResponse
from src.schemas.country import CountrySchemaResponse


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest_asyncio.fixture(scope="function")
async def db_engine(postgres_container):
    engine = create_async_engine(
        postgres_container.get_connection_url(driver="asyncpg")
    )
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    from src.models.base import Base
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    SessionFactory = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    try:
        async with SessionFactory() as session:
            yield session
    finally:
        async with db_engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7") as container:
        yield container


@pytest_asyncio.fixture(scope="function")
async def redis_client(redis_container):
    client = Redis(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379),
        decode_responses=True
    )
    yield client
    await client.flushall()
    await client.aclose()


@pytest.fixture(scope="function")
def db_session_factory(db_engine):
    SessionFactory = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return SessionFactory


@pytest.fixture(scope="function")
def test_app(redis_client, db_session_factory, db_session):
    app = get_app()

    def return_redis():
        return redis_client

    async def override_read_session():
        async with db_session_factory() as session:
            yield session

    def override_uow():
        return UnitOfWork(db_session_factory)

    app.dependency_overrides[get_redis] = return_redis
    app.dependency_overrides[get_read_session] = override_read_session
    app.dependency_overrides[get_book_uow] = override_uow
    app.dependency_overrides[get_course_uow] = override_uow
    app.dependency_overrides[get_country_uow] = override_uow
    yield app


@pytest_asyncio.fixture(scope="function")
async def http_client(test_app):
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def entities_data(db_session):
    author1 = AuthorModel(
        name='Fifiv',
        age=25,
        location='Mock',
        citizenship='Da',
    )
    author2 = AuthorModel(
        name='Fafav',
        age=28,
        location='Fack',
        citizenship='Net',
    )
    author1.id = uuid.uuid4()
    author2.id = uuid.uuid4()
    book = BookModel(
        title='Mima',
        description='test',
        genre=['horror', 'rom', 'fan'],
        date_written=date(2026, 9, 16),
        authors=[author1, author2],
    )
    book.id = uuid.uuid4()

    student1 = StudentModel(
        name='masha',
        age=15,
        dormitory='Mic',
        citizenship='Nick',
    )
    student2 = StudentModel(
        name='Gelya',
        age=35,
        dormitory='Dak',
        citizenship='Rick',
    )
    student1.id = uuid.uuid4()
    student2.id = uuid.uuid4()
    course = CourseModel(
        title='Fafa',
        description='Fifi',
        mentor='Ababa',
        teaching_hours=210,
        students=[student1, student2],
    )
    course.id = uuid.uuid4()

    capital = CapitalModel(
        name='DAWA',
        mayor='Hz',
        population=134,
    )
    capital.id = uuid.uuid4()
    country = CountryModel(
        name='Darada',
        president='Mimka',
        population=1231,
        currency='weq',
        capital=capital,
    )
    country.id = uuid.uuid4()
    db_session.add(country)
    db_session.add(course)
    db_session.add(book)
    await db_session.commit()

    obj_dict = {
        'book':
            {
                'id': book.id,
                'data': BookSchemaResponse.model_validate(book).model_dump(mode="json"),
            },
        'course':
            {
                'id': course.id,
                'data': CourseSchemaResponse.model_validate(course).model_dump(mode="json"),
            },
        'country':
            {
                'id': country.id,
                'data': CountrySchemaResponse.model_validate(country).model_dump(mode="json"),
            },
    }
    return obj_dict
