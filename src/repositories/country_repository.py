from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.countries import CountryModel


async def create(session: AsyncSession, country: CountryModel):
    session.add(country)
    await session.flush()
    return country


async def find_country(session: AsyncSession, country_id: UUID):
    query = (
        select(CountryModel)
        .where(CountryModel.id == country_id)
        .where(CountryModel.is_deleted == False)
        .options(selectinload(CountryModel.capital))
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()
