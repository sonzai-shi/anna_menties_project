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


class CountryService:
    def __init__(self, session: AsyncSession):
        self.country_repo = Repository(session)

    async def create_country(self, country_data: CountrySchemaCreate) -> CountrySchemaResponse:
        country = country_mapper.to_model(country_data)
        result = await self.country_repo.create(country)
        return CountrySchemaResponse.model_validate(result)

    async def read_country(self, country_id: UUID) -> CountrySchemaResponse:
        result = await self.find_country(country_id)
        return CountrySchemaResponse.model_validate(result)

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
        return country_mapper.to_pagination(
            countries=result,
            limit=limit,
            next_cursor_created_at=next_cursor_created_at,
            next_cursor_id=next_cursor_id,
        )

    async def update_country(self, country_id: UUID, data: CountrySchemaUpdate) -> CountrySchemaResponse:
        country = await self.find_country(country_id)
        await self.country_repo.update_one(CountryModel, country_id, 'capital', data)
        return CountrySchemaResponse.model_validate(country)

    async def delete_country(self, country_id: UUID) -> str:
        result = await self.find_country(country_id)
        result.is_deleted = True
        result.capital.is_deleted = True
        return f'Country with ID: {country_id} has been removed.'

    async def find_country(self, country_id: UUID) -> CountryModel:
        result = await self.country_repo.find_one(CountryModel, country_id, 'capital')
        if result is None:
            raise ObjectNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Country with ID: {country_id} not found.'
            )
        return result
