import uuid
import pytest


@pytest.mark.parametrize('resource', ['book', 'course', 'country'])
@pytest.mark.asyncio
async def test_read_not_found(http_client, resource):
    obj_id = uuid.uuid4()
    path = f'/v1/{resource}/{obj_id}'
    result = await http_client.get(path)
    assert result.status_code == 404


@pytest.mark.parametrize('resource', ['book', 'course', 'country'])
@pytest.mark.asyncio
async def test_read_found(http_client, resource, entities_data):
    entity = entities_data[resource]
    entity_id = entity['id']
    path = f'/v1/{resource}/{entity_id}'
    result = await http_client.get(path)
    assert result.status_code == 200
    assert result.json() == entity['data']



@pytest.mark.parametrize('resource', ['book', 'course', 'country'])
@pytest.mark.asyncio
async def test_read_found_many(http_client, resource, entities_data):
    entity = entities_data[resource]
    entity_id = entity['id']
    path = f'/v1/{resource}'
    result = await http_client.get(path, params={'limit': 10})
    assert result.status_code == 200
    page = result.json()
    assert page['items'] == [entity['data']]
    assert page['limit'] == 10
    assert page['next_cursor_id'] == str(entity_id)


@pytest.mark.parametrize('resource', ['book', 'course', 'country'])
@pytest.mark.asyncio
async def test_delete(http_client, resource, entities_data):
    entity = entities_data[resource]
    entity_id = entity['id']
    path = f'/v1/{resource}/{entity_id}'
    result = await http_client.delete(path)
    assert result.status_code == 204
    assert result.content == b''

    result = await http_client.get(path)
    assert result.status_code == 404


@pytest.mark.parametrize(
    'resource, update_data',
    [('book', {'title':'Dari'}),
     ('course', {'title':'Rari'}),
     ('country', {'name':'Fari'})])
@pytest.mark.asyncio
async def test_update(http_client, resource, entities_data, update_data):
    entity = entities_data[resource]
    entity_id = entity['id']
    path = f'/v1/{resource}/{entity_id}'
    result = await http_client.put(path, json=update_data)
    assert result.status_code == 200
    for field, data in update_data.items():
        assert result.json()[field] == data
