from uuid import UUID
from redis.asyncio import Redis


class RedisCache:
    def __init__(self, redis: Redis):
        self.cache = redis

    async def set(self, model_name: str, key: UUID, value: str) -> None:
        await self.cache.set(f'{model_name}:{key}', value, ex=3600)

    async def get(self, model_name: str, key: UUID) -> bytes | str | None:
        return await self.cache.get(f'{model_name}:{key}')

    async def delete(self, model_name: str, key: UUID) -> int:
        return await self.cache.delete(f'{model_name}:{key}')

    async def sets(self, model_name: str, data: dict[UUID, str]) -> None:
        for book_id, book in data.items():
            await self.set(
                model_name=model_name,
                key=book_id,
                value=book,
            )
