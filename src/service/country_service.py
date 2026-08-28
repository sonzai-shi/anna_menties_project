from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.capitals import CapitalModel
from src.models.countries import CountryModel
from src.schemas.country import CountrySchemaCreate, CountrySchemaResponse, CountrySchemaUpdate, CountrySchemaPagination
from src.repositories.repository import Repository

class CountryService:
    def __init__(self, session: AsyncSession):
        self.country_repo = Repository(session)


    async def create_country(self, country_data: CountrySchemaCreate):
        country = CountryModel(
            name=country_data.name,
            president=country_data.president,
            population=country_data.population,
            currency=country_data.currency
        )
        capital = CapitalModel(
            name=country_data.capital.name,
            mayor=country_data.capital.mayor,
            population=country_data.capital.population,
        )
        country.capital = capital
        result = await self.country_repo.create(country)
        return CountrySchemaResponse.model_validate(result)


    async def read_country(self, country_id: UUID):
        result = await self.find_country(country_id)
        return CountrySchemaResponse.model_validate(result)


    async def read_countries(self, offset: int, limit: int):
        result = await self.country_repo.find_many(CountryModel,'capital', offset, limit)
        return CountrySchemaPagination(
            items=[CountrySchemaResponse.model_validate(country) for country in result],
            offset=offset,
            limit=limit,
        )


    async def update_country(self, country_id: UUID, data: CountrySchemaUpdate):
        country = await self.find_country(country_id)

        if data.name is not None:
            country.name = data.name
        if data.president is not None:
            country.president = data.president
        if data.population is not None:
            country.population = data.population
        if data.currency is not None:
            country.currency = data.currency

        if data.capital is not None:
            if data.capital.name is not None:
                country.capital.name = data.capital.name
            if data.capital.mayor is not None:
                country.capital.mayor = data.capital.mayor
            if data.capital.population is not None:
                country.capital.population = data.capital.population

        return CountrySchemaResponse.model_validate(country)


    async def delete_country(self, country_id: UUID):
        result = await self.find_country(country_id)
        result.is_deleted = True
        result.capital.is_deleted = True
        return 'The country has been removed.'


    async def find_country(self, country_id: UUID):
        result = await self.country_repo.find_one(CountryModel, country_id, 'capital')
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Country not found.'
            )
        return result