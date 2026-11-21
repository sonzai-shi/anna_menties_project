from uuid import UUID
from redis.asyncio import Redis
from src.config import settings


class RedisCache:
    def __init__(self, redis: Redis):
        self.cache = redis

    async def set(self, model_name: str, key: UUID | str, value: str) -> None:
        await self.cache.set(f'{model_name}:{key}', value, ex=settings.redis_cache_ttl)

    async def get(self, model_name: str, key: UUID | str) -> bytes | str | None:
        return await self.cache.get(f'{model_name}:{key}')

    async def delete(self, model_name: str, key: UUID) -> int:
        return await self.cache.delete(f'{model_name}:{key}')

    async def sets(self, model_name: str, data: dict[UUID, str]) -> None:
        async with self.cache.pipeline() as pipe:
            for key, value in data.items():
                pipe.set(f'{model_name}:{key}', value, ex=settings.redis_cache_ttl)
            await pipe.execute()

    async def delete_all_pages(self, pattern: str) -> None:
        keys = []
        async for item in self.cache.scan_iter(match=pattern):
            keys.append(item)
        if keys:
            await self.cache.delete(*keys)