from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.capitals import CapitalModel
from src.models.countries import CountryModel
from src.schemas.country import CountrySchemaCreate, CountrySchemaResponse, CountrySchemaUpdate, CountrySchemaPagination
from src.repositories import country_repository as country_repo


async def create_country(country_data: CountrySchemaCreate, session: AsyncSession):
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
    result = await country_repo.create(session, country)
    return CountrySchemaResponse.model_validate(result)


async def find_country(country_id: UUID, session: AsyncSession):
    result = await country_repo.find_country(session, country_id)
    if result is None:
        return None
    return CountrySchemaResponse.model_validate(result)


async def find_countries(offset: int, limit: int, session: AsyncSession):
    result = await country_repo.find_countries(session, offset, limit)
    if result is None:
        return None
    return CountrySchemaPagination(
        items=[CountrySchemaResponse.model_validate(country) for country in result],
        offset=offset,
        limit=limit,
    )


async def update_country(country_id: UUID, data: CountrySchemaUpdate, session: AsyncSession):
    country = await country_repo.find_country(session, country_id)
    if country is None:
        return None

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


async def delete_country(country_id: UUID, session: AsyncSession):
    result = await country_repo.find_country(session, country_id)
    if result is None:
        return None
    result.is_deleted = True
    result.capital.is_deleted = True
    return True