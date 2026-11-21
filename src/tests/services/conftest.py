import uuid
from datetime import date
import pytest

from src.service.country_service import CountryService
from src.service.course_service import CourseService
from src.service.book_service import BookService
from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.models.students import StudentModel
from src.models.courses import CourseModel
from src.models.capitals import CapitalModel
from src.models.countries import CountryModel
from src.schemas.book import BookSchemaResponse, BookSchemaUpdate
from src.schemas.course import CourseSchemaResponse, CourseSchemaUpdate
from src.schemas.country import CountrySchemaResponse, CountrySchemaUpdate
from src.schemas.book import BookSchemaPagination
from src.schemas.course import CourseSchemaPagination
from src.schemas.country import CountrySchemaPagination


@pytest.fixture(scope="function")
def book():
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
    return book


@pytest.fixture(scope="function")
def course():
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
    return course


@pytest.fixture(scope="function")
def country():
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
    return country


@pytest.fixture(scope="function", params=['book', 'course', 'country'])
def entity(request):
    schema_response = {
        'book': BookSchemaResponse,
        'course': CourseSchemaResponse,
        'country': CountrySchemaResponse,
    }
    read_method = {
        'book': "read_book",
        'course': "read_course",
        'country': "read_country",
    }
    many_read_method = {
        'book': 'read_books',
        'course': 'read_courses',
        'country': 'read_countries',
    }
    service_class = {
        'book': BookService,
        'course': CourseService,
        'country': CountryService,
    }
    page_schema = {
        'book': BookSchemaPagination,
        'course': CourseSchemaPagination,
        'country': CountrySchemaPagination,
    }
    delete_methods = {
        'book': 'delete_book',
        'course': 'delete_course',
        'country': 'delete_country',
    }
    update_schemas = {
        'book': BookSchemaUpdate,
        'course': CourseSchemaUpdate,
        'country': CountrySchemaUpdate,
    }
    update_methods = {
        'book': 'update_book',
        'course': 'update_course',
        'country': 'update_country',
    }
    update_data = {
        'book': {'title': 'Updated Book'},
        'course': {'title': 'Updated Course'},
        'country': {'name': 'Updated Country'},
    }
    return {
        'name': request.param,
        'object': request.getfixturevalue(request.param),
        'schema': schema_response[request.param],
        'read_method': read_method[request.param],
        'service_class': service_class[request.param],
        'many_read_method': many_read_method[request.param],
        'page_schema': page_schema[request.param],
        'delete_method': delete_methods[request.param],
        'update_schema': update_schemas[request.param],
        'update_method': update_methods[request.param],
        'update_data': update_data[request.param],
    }
