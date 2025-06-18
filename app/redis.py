from functools import wraps
import json
from typing import Callable, Type
from redis import Redis
import redis.asyncio as redis
from pydantic import BaseModel

redis_client = redis.Redis(
    host="redis",  # или "redis", если внутри Docker-сети
    port=6379,
    decode_responses=True  # чтобы возвращать строки, а не байты
)


def redis_cache(
    schema: Type[BaseModel],
    redis: Redis = redis_client,
    expire: int = 3600
):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = kwargs.get("key")
            if not key:
                raise ValueError("Missing 'key' argument for caching.")

            cached = await redis.get(key)
            if cached:
                return schema(**json.loads(cached))

            result = await func(*args, **kwargs)
            if result:
                await redis.set(key, schema.from_orm(result).model_dump_json(), ex=expire)
            return result
        return wrapper
    return decorator