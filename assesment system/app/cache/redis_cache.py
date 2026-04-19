import redis
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)


def set_cache(key: str, value: str, expire: int = 300):
    redis_client.set(key, value, ex=expire)


def get_cache(key: str):
    value = redis_client.get(key)
    return value.decode("utf-8") if value else None