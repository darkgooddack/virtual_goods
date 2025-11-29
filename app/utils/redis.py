from redis.asyncio import Redis
import json
from typing import Any
from app.core.config import settings
import redis.exceptions


class RedisCache:
    def __init__(self):
        self.redis = Redis.from_url(
            settings.redis.url,
            decode_responses=True
        )

    async def get(self, key: str) -> Any:
        data = await self.redis.get(key)
        if data is None:
            return None
        return json.loads(data)

    async def set(self, key: str, value: Any, expire: int = 300):
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def check_redis(self) -> bool:
        try:
            pong = await self.redis.ping()
            return bool(pong)
        except redis.exceptions.RedisError:
            return False


redis_cache = RedisCache()
