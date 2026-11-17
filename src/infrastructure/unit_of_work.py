from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            await self.session.rollback()
        else:
            try:
                await self.session.commit()
            except Exception:
                await self.session.rollback()
                raise
