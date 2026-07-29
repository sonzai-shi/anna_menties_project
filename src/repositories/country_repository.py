from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.db import get_session
from src.models.capitals import CapitalModel
from src.models.countries import CountryModel
from src.schemas.country import CountrySchemaCreate


async def create_country(country_data: CountrySchemaCreate):
    async with get_session() as session:
        db_country = CountryModel(name=country_data.country_name)
        db_country.capital = CapitalModel(name=country_data.capital.capital_name)

        session.add(db_country)
        await session.flush()

        return {
            'id': db_country.id,
            'country_name': db_country.name,
            'capital': {
                'id': db_country.capital.id,
                'capital_name': db_country.capital.name
            }
        }


async def find_country(country_id: UUID):
    async with get_session() as session:
        country = await _find(session, country_id)
        if country is None:
            return None
        return {
            'id': country.id,
            'country_name': country.name,
            'capital': {
                'id': country.capital.id,
                'capital_name': country.capital.name,
            }
        }


async def update_country(country_data: CountrySchemaCreate, country_id: UUID):
    async with get_session() as session:
        country = await _find(session, country_id)
        if country is None:
            return None

        country.name = country_data.country_name
        country.capital.name = country_data.capital.capital_name
        return {
            'id': country.id,
            'country_name': country.name,
            'capital': {
                'id': country.capital.id,
                'capital_name': country.capital.name,
            }
        }


async def delete_country(country_id: UUID):
    async with get_session() as session:
        country = await _find(session, country_id)
        if country is None:
            return None
        country.is_deleted = True
        country.capital.is_deleted = True
        return True


async def _find(session, country_id: UUID):
        query = (
            select(CountryModel)
            .where(CountryModel.id == country_id)
            .where(CountryModel.is_deleted == False)
            .options(selectinload(CountryModel.capital))
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()


