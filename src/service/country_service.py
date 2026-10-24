from uuid import UUID
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.mappers import country_mapper
from src.models.countries import CountryModel
from src.schemas.country import (
    CountrySchemaCreate,
    CountrySchemaResponse,
    CountrySchemaUpdate,
    CountrySchemaPagination,
)
from datetime import datetime
from src.repositories.repository import Repository
from src.exceptions.service_exception import ObjectNotFoundException, CursorException
from src.cache.redis_cache import RedisCache
from redis.asyncio import Redis
from src.unit_of_work import UnitOfWork


class CountryService:
    def __init__(
            self,
            redis: Redis,
            session: AsyncSession | None = None,
            uow: UnitOfWork | None = None,
    ) -> None:
        if session is not None:
            self.country_repo = Repository(session)
            self.uow = None
        else:
            self.country_repo = None
            self.uow = uow
        self.country_redis = RedisCache(redis)

    async def create_country(self, country_data: CountrySchemaCreate) -> CountrySchemaResponse:
        async with self.uow as uow:
            local_country_repo = Repository(uow.session)
            country = country_mapper.to_model(country_data)
            result = await local_country_repo.create(country)
            schema_response = CountrySchemaResponse.model_validate(result)
        return schema_response

    async def read_country(self, country_id: UUID) -> CountrySchemaResponse:
        result_cache = await self.country_redis.get(model_name='country', key=country_id)
        if result_cache:
            return CountrySchemaResponse.model_validate_json(result_cache)
        result = await self.find_country(country_id)
        schema_response = CountrySchemaResponse.model_validate(result)
        await self.country_redis.set(model_name='country', key=country_id, value=schema_response.model_dump_json())
        return schema_response

    async def read_countries(
            self,
            limit: int,
            cursor_created_at: datetime | None,
            cursor_id: UUID | None,
    ) -> CountrySchemaPagination:
        if (cursor_created_at is None) != (cursor_id is None):
            raise CursorException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'You must provide both cursor_created_at and cursor_id.'
            )
        result = await self.country_repo.find_many(
            model=CountryModel,
            join_orm='capital',
            limit=limit,
            cursor_created_at=cursor_created_at,
            cursor_id=cursor_id,
        )
        next_cursor_created_at = None
        next_cursor_id = None

        if result:
            last_country = result[-1]
            next_cursor_created_at = last_country.created_at
            next_cursor_id = last_country.id

        country_cache_data = {
            country.id:
                CountrySchemaResponse
                .model_validate(country)
                .model_dump_json()
            for country in result
        }
        await self.country_redis.sets(model_name='country', data=country_cache_data, )

        return country_mapper.to_pagination(
            countries=result,
            limit=limit,
            next_cursor_created_at=next_cursor_created_at,
            next_cursor_id=next_cursor_id,
        )

    async def update_country(self, country_id: UUID, data: CountrySchemaUpdate) -> CountrySchemaResponse:
        async with self.uow as uow:
            local_country_repo = Repository(uow.session)
            country = await local_country_repo.find_one(CountryModel, country_id, 'capital')
            if country is None:
                self.raise_country_not_found(country_id)
            await local_country_repo.update_one(CountryModel, country_id, 'capital', data)
            schema_response = CountrySchemaResponse.model_validate(country)
        await self.country_redis.set(model_name='country', key=country_id, value=schema_response.model_dump_json())
        return schema_response

    async def delete_country(self, country_id: UUID) -> str:
        async with self.uow as uow:
            local_country_repo = Repository(uow.session)
            result = await local_country_repo.find_one(CountryModel, country_id, 'capital')
            if result is None:
                self.raise_country_not_found(country_id)
            result.is_deleted = True
            result.capital.is_deleted = True
        return f'Country with ID: {country_id} has been removed.'

    async def find_country(self, country_id: UUID) -> CountryModel:
        result = await self.country_repo.find_one(CountryModel, country_id, 'capital')
        if result is None:
            self.raise_country_not_found(country_id)
        return result

    def raise_country_not_found(self, country_id: UUID):
        raise ObjectNotFoundException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Country with ID: {country_id} not found.'
        )
