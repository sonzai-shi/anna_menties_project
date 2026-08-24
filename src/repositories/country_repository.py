from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.countries import CountryModel

class CountryRepository():
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, country: CountryModel):
        self.session.add(country)
        await self.session.flush()
        return country


    async def find_country(self, country_id: UUID):
        query = (
            select(CountryModel)
            .where(CountryModel.id == country_id)
            .where(CountryModel.is_deleted == False)
            .options(selectinload(CountryModel.capital))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def find_countries(self, offset: int, limit: int):
        query = (
            select(CountryModel)
            .where(CountryModel.is_deleted == False)
            .options(selectinload(CountryModel.capital))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
