from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, model):
        self.session.add(model)
        await self.session.flush()
        return model


    async def find_one(self, model, id_model: UUID, join_orm):
        query = (
            select(model)
            .where(model.id == id_model)
            .where(model.is_deleted == False)
            .options(selectinload(getattr(model, join_orm)))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def find_many(self, model, join_orm, offset: int, limit: int):
        query = (
            select(model)
            .where(model.is_deleted == False)
            .options(selectinload(getattr(model, join_orm)))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()