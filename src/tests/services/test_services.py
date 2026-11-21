import uuid
import pytest
from src.config import settings
from src.infrastructure.redis_cache import RedisCache
from src.repositories.repository import Repository
from src.exceptions.service_exception import ObjectNotFoundException
from src.infrastructure.unit_of_work import UnitOfWork


@pytest.mark.asyncio
async def test_empty_cache(entity, db_session, redis_client):
    orm_obj = entity['object']
    db_session.add(orm_obj)
    await db_session.commit()

    repository = Repository(db_session)
    redis = RedisCache(redis_client)
    uow = UnitOfWork(db_session)
    service = entity['service_class'](repository=repository, redis=redis, uow=uow)

    cache = await redis.get(model_name=entity['name'], key=orm_obj.id)
    assert cache is None
    read_method = getattr(service, entity['read_method'])

    result = await read_method(orm_obj.id)
    expected_response = entity['schema'].model_validate(orm_obj)
    assert result == expected_response

    cache = await redis.get(model_name=entity['name'], key=orm_obj.id)
    assert cache is not None
    cache = entity['schema'].model_validate_json(cache)
    assert cache == expected_response

    ttl = await redis_client.ttl(name=f'{entity['name']}:{orm_obj.id}')
    assert 0 < ttl <= settings.redis_cache_ttl


@pytest.mark.asyncio
async def test_in_cache(entity, db_session, redis_client):
    orm_obj = entity['object']

    repository = Repository(db_session)
    redis = RedisCache(redis_client)
    uow = UnitOfWork(db_session)
    service = entity['service_class'](repository=repository, redis=redis, uow=uow)

    response = entity['schema'].model_validate(orm_obj)
    response_json = response.model_dump_json()
    await redis_client.set(name=f'{entity['name']}:{orm_obj.id}', value=response_json, ex=settings.redis_cache_ttl)

    read_method = getattr(service, entity['read_method'])
    result = await read_method(orm_obj.id)
    assert result == response


@pytest.mark.asyncio
async def test_not_found(entity, db_session, redis_client):
    object_id = uuid.uuid4()
    repository = Repository(db_session)
    redis = RedisCache(redis_client)
    uow = UnitOfWork(db_session)
    service = entity['service_class'](repository=repository, redis=redis, uow=uow)
    read_method = getattr(service, entity['read_method'])
    with pytest.raises(ObjectNotFoundException):
        await read_method(object_id)
    cache = await redis.get(model_name=entity['name'], key=object_id)
    assert cache is None


@pytest.mark.asyncio
async def test_list_with_empty_page_cache(entity, db_session, redis_client):
    orm_obj = entity['object']
    db_session.add(orm_obj)
    await db_session.commit()

    repository = Repository(db_session)
    redis = RedisCache(redis_client)
    uow = UnitOfWork(db_session)
    service = entity['service_class'](repository=repository, redis=redis, uow=uow)

    limit = 10
    page_key = f'page:{limit}:None:None'
    redis_key = f"{entity['name']}:page:{limit}:None:None"

    cache = await redis.get(model_name=entity['name'], key=page_key)
    assert cache is None

    many_read_method = getattr(service, entity['many_read_method'])
    result = await many_read_method(limit=limit, cursor_created_at=None, cursor_id=None)

    expected_item = entity['schema'].model_validate(orm_obj)
    assert result.items == [expected_item]
    assert result.limit == limit
    assert result.next_cursor_id == orm_obj.id
    assert result.next_cursor_created_at == orm_obj.created_at

    cache_page = await redis.get(model_name=entity['name'], key=page_key)
    assert cache_page is not None
    cache_page_model = entity['page_schema'].model_validate_json(cache_page)
    assert cache_page_model == result

    ttl = await redis_client.ttl(redis_key)
    assert 0 < ttl <= settings.redis_cache_ttl


@pytest.mark.asyncio
async def test_empty_list(entity, db_session, redis_client):
    repository = Repository(db_session)
    redis = RedisCache(redis_client)
    uow = UnitOfWork(db_session)
    service = entity['service_class'](repository=repository, redis=redis, uow=uow)

    limit = 10
    page_key = f'page:{limit}:None:None'
    redis_key = f"{entity['name']}:page:{limit}:None:None"

    many_read_method = getattr(service, entity['many_read_method'])
    result = await many_read_method(limit=limit, cursor_created_at=None, cursor_id=None)
    assert result.items == []
    assert result.limit == limit
    assert result.next_cursor_id is None
    assert result.next_cursor_created_at is None

    cache_page = await redis.get(model_name=entity['name'], key=page_key)
    assert cache_page is not None
    cache_page_model = entity['page_schema'].model_validate_json(cache_page)
    assert cache_page_model == result

    ttl = await redis_client.ttl(redis_key)
    assert 0 < ttl <= settings.redis_cache_ttl


@pytest.mark.asyncio
async def test_update_object(entity, db_session, redis_client):
    orm_obj = entity['object']
    db_session.add(orm_obj)
    await db_session.commit()

    repository = Repository(db_session)
    redis = RedisCache(redis_client)
    uow = UnitOfWork(db_session)
    service = entity['service_class'](repository=repository, redis=redis, uow=uow)

    update_data = entity['update_data']
    update_payload = entity['update_schema'](**update_data)

    update_method = getattr(service, entity['update_method'])
    result = await update_method(orm_obj.id, update_payload)

    assert result.id == orm_obj.id
    for field, value in update_data.items():
        assert getattr(result, field) == value

    await db_session.refresh(orm_obj)
    for field, value in update_data.items():
        assert getattr(orm_obj, field) == value


@pytest.mark.asyncio
async def test_delete_object(entity, db_session, redis_client):
    orm_obj = entity['object']
    db_session.add(orm_obj)
    await db_session.commit()

    repository = Repository(db_session)
    redis = RedisCache(redis_client)
    uow = UnitOfWork(db_session)
    service = entity['service_class'](repository=repository, redis=redis, uow=uow)

    delete_method = getattr(service, entity['delete_method'])
    await delete_method(orm_obj.id)

    await db_session.refresh(orm_obj)
    assert orm_obj.is_deleted is True

    read_method = getattr(service, entity['read_method'])
    with pytest.raises(ObjectNotFoundException):
        await read_method(orm_obj.id)
