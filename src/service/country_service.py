from uuid import UUID
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.mappers import country_mapper
from src.models.countries import CountryModel
from src.schemas.country import (
    CountrySchemaCreate,
    CountrySchemaResponse,
    CountrySchemaUpdate,
)
from src.repositories.repository import Repository
from src.exceptions.service_exception import ObjectNotFoundException


class CountryService:
    def __init__(self, session: AsyncSession):
        self.country_repo = Repository(session)

    async def create_country(self, country_data: CountrySchemaCreate):
        country = country_mapper.to_model(country_data)
        result = await self.country_repo.create(country)
        return CountrySchemaResponse.model_validate(result)

    async def read_country(self, country_id: UUID):
        result = await self.find_country(country_id)
        return CountrySchemaResponse.model_validate(result)

    async def read_countries(self, offset: int, limit: int):
        result = await self.country_repo.find_many(CountryModel, 'capital', offset, limit)
        return country_mapper.to_pagination(countries=result, offset=offset, limit=limit)

    async def update_country(self, country_id: UUID, data: CountrySchemaUpdate):
        country = await self.find_country(country_id)
        country_mapper.update_country(country, data)
        return CountrySchemaResponse.model_validate(country)

    async def delete_country(self, country_id: UUID):
        result = await self.find_country(country_id)
        result.is_deleted = True
        result.capital.is_deleted = True
        return f'Country with ID: {country_id} has been removed.'

    async def find_country(self, country_id: UUID):
        result = await self.country_repo.find_one(CountryModel, country_id, 'capital')
        if result is None:
            raise ObjectNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Country with ID: {country_id} not found.'
            )
        return result
