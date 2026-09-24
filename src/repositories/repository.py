from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update


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

    async def update_one(self, model, id_model, join_orm, data):
        update_data = data.model_dump(exclude_unset=True)
        join_orm_data = update_data.pop(join_orm, None)

        if update_data:
            query = (
                update(model)
                .where(model.id == id_model)
                .values(**update_data)
            )
            await self.session.execute(query)

        if join_orm_data is not None:
            join_model = getattr(model, join_orm).property.mapper.class_

            if isinstance(join_orm_data, dict):
                join_id = join_orm_data["id"]
                query = (
                    update(join_model)
                    .where(join_model.id == join_id)
                    .values(**join_orm_data)
                )
                await self.session.execute(query)

            else:
                for nested_data in join_orm_data:
                    join_id = nested_data["id"]
                    query = (
                        update(join_model)
                        .where(join_model.id == join_id)
                        .values(**nested_data)
                    )
                    await self.session.execute(query)
