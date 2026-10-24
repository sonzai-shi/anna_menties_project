import uuid
import pytest
from src.unit_of_work import UnitOfWork
from src.exceptions.service_exception import ObjectNotFoundException
from src.schemas.course import CourseSchemaResponse, CourseSchemaUpdate
from src.service.course_service import CourseService
from src.models.students import StudentModel
from src.models.courses import CourseModel


@pytest.mark.asyncio
async def test_empty_cache(db_session, redis_client):
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
    db_session.add(course)
    await db_session.commit()
    result = await redis_client.get(name=f'course:{course.id}')
    assert result is None

    service = CourseService(session=db_session, redis=redis_client, uow=None)
    schema_response = await service.read_course(course.id)

    assert schema_response.id == course.id
    assert schema_response.title == 'Fafa'
    assert schema_response.description == 'Fifi'
    assert schema_response.mentor == 'Ababa'
    assert schema_response.teaching_hours == 210
    ids_response = [student.id for student in schema_response.students]
    assert len(ids_response) == 2
    assert student1.id in ids_response
    assert student2.id in ids_response

    course_cache = await redis_client.get(name=f'course:{course.id}')
    assert course_cache is not None
    course_cache = CourseSchemaResponse.model_validate_json(course_cache)

    assert course_cache.id == course.id
    assert course_cache.title == 'Fafa'
    assert course_cache.description == 'Fifi'
    assert course_cache.mentor == 'Ababa'
    assert course_cache.teaching_hours == 210
    ids_response = [student.id for student in course_cache.students]
    assert len(ids_response) == 2
    assert student1.id in ids_response
    assert student2.id in ids_response
    course_ttl = await redis_client.ttl(name=f'course:{course.id}')
    assert 0 < course_ttl <= 3600


@pytest.mark.asyncio
async def test_course_in_cache(db_session, redis_client):
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

    schema_response = CourseSchemaResponse.model_validate(course)
    await redis_client.set(name=f'course:{course.id}', value=schema_response.model_dump_json(), ex=3600)

    service = CourseService(session=db_session, redis=redis_client, uow=None)
    schema_response = await service.read_course(course.id)

    assert schema_response is not None
    assert schema_response.id == course.id
    assert schema_response.title == course.title
    assert schema_response.description == course.description
    assert schema_response.mentor == course.mentor
    assert schema_response.teaching_hours == course.teaching_hours
    ids_response = [student.id for student in schema_response.students]
    assert student1.id in ids_response
    assert student2.id in ids_response
    assert len(ids_response) == 2
    course_ttl = await redis_client.ttl(name=f'course:{course.id}')
    assert 0 < course_ttl <= 3600


@pytest.mark.asyncio
async def test_course_not_found(db_session, redis_client):
    course_id = uuid.uuid4()
    service = CourseService(session=db_session, redis=redis_client, uow=None)
    with pytest.raises(ObjectNotFoundException):
        await service.read_course(course_id)
    result = await redis_client.get(name=f'course:{course_id}')
    assert result is None


@pytest.mark.asyncio
async def test_many_courses(db_session, redis_client):
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
    course1 = CourseModel(
        title='Fafa',
        description='Fifi',
        mentor='Ababa',
        teaching_hours=210,
        students=[student1, student2],
    )
    course1.id = uuid.uuid4()
    student3 = StudentModel(
        name='Fad',
        age=32,
        dormitory='dfasf',
        citizenship='WD',
    )
    student4 = StudentModel(
        name='Fww',
        age=34,
        dormitory='sdf',
        citizenship='Fas',
    )
    student3.id = uuid.uuid4()
    student4.id = uuid.uuid4()
    course2 = CourseModel(
        title='Wewe',
        description='Frws',
        mentor='Ababa',
        teaching_hours=343,
        students=[student3, student4],
    )
    course2.id = uuid.uuid4()
    db_session.add(course1)
    db_session.add(course2)
    await db_session.commit()

    service = CourseService(session=db_session, redis=redis_client, uow=None)

    result_schema_response = await service.read_courses(limit=2, cursor_created_at=None, cursor_id=None)
    assert result_schema_response is not None
    assert len(result_schema_response.items) == 2
    ids_response = [course.id for course in result_schema_response.items]
    assert course1.id in ids_response
    assert course2.id in ids_response

    for course_response in result_schema_response.items:
        course_cache = await redis_client.get(name=f'course:{course_response.id}')
        assert course_cache is not None
        course_cache = CourseSchemaResponse.model_validate_json(course_cache)
        assert course_response.id == course_cache.id
        assert course_response.title == course_cache.title
        assert course_response.description == course_cache.description
        assert course_response.mentor == course_cache.mentor
        assert course_response.teaching_hours == course_cache.teaching_hours
        assert course_response.students == course_cache.students
        ttl_id = await redis_client.ttl(name=f'course:{course_response.id}')
        assert 0 < ttl_id <= 3600


@pytest.mark.asyncio
async def test_many_courses_not_found(db_session, redis_client):
    service = CourseService(session=db_session, redis=redis_client, uow=None)
    result_schema_response = await service.read_courses(limit=2, cursor_created_at=None, cursor_id=None)
    assert len(result_schema_response.items) == 0
    assert result_schema_response.next_cursor_id is None
    assert result_schema_response.next_cursor_created_at is None
    assert result_schema_response.limit == 2

    id_list = []
    async for key in redis_client.scan_iter(match='course:*'):
        id_list.append(key)
    assert len(id_list) == 0


@pytest.mark.asyncio
async def test_update_courses(db_session, db_session_factory, redis_client):
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
    db_session.add(course)
    await db_session.commit()

    uow = UnitOfWork(session_factory=db_session_factory)
    service = CourseService(session=None, redis=redis_client, uow=uow)
    schema_response = CourseSchemaResponse.model_validate(course)
    await redis_client.set(name=f'course:{course.id}', value=schema_response.model_dump_json(), ex=3600)
    course_update = CourseSchemaUpdate(title='Kizil')
    result_update = await service.update_course(course.id, course_update)

    assert result_update is not None
    assert result_update.id == course.id
    assert result_update.title == 'Kizil'
    assert result_update.description == 'Fifi'
    assert result_update.mentor == 'Ababa'
    assert result_update.teaching_hours == 210
    ids_result_update = [student.id for student in result_update.students]
    assert len(ids_result_update) == 2
    assert student1.id in ids_result_update
    assert student2.id in ids_result_update

    course_update_cache = await redis_client.get(name=f'course:{course.id}')
    assert course_update_cache is not None
    course_update_cache = CourseSchemaResponse.model_validate_json(course_update_cache)
    assert course_update_cache is not None
    assert course_update_cache.id == course.id
    assert course_update_cache.title == 'Kizil'
    assert course_update_cache.description == 'Fifi'
    assert course_update_cache.mentor == 'Ababa'
    assert course_update_cache.teaching_hours == 210
    ids_response = [students.id for students in course_update_cache.students]
    assert len(ids_response) == 2
    assert student1.id in ids_response
    assert student2.id in ids_response
    ttl_id = await redis_client.ttl(name=f'course:{course.id}')
    assert 0 < ttl_id <= 3600

@pytest.mark.asyncio
async def test_update_not_found_course(db_session, db_session_factory, redis_client):
    course_id = uuid.uuid4()
    uow = UnitOfWork(session_factory=db_session_factory)
    service = CourseService(session=None, redis=redis_client, uow=uow)
    with pytest.raises(ObjectNotFoundException):
        await service.update_course(course_id, CourseSchemaUpdate(title='Kizil'))
    result = await redis_client.get(name=f'course:{course_id}')
    assert result is None
