import redis.asyncio as redis

redis_client = redis.Redis(
    host="redis",  # или "redis", если внутри Docker-сети
    port=6379,
    decode_responses=True  # чтобы возвращать строки, а не байты
)
