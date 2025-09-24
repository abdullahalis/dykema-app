# cache/redis_cache.py
import json
from storage.cache.base_cache import CacheManager
from config.services import redis

class RedisCacheManager(CacheManager):
    def __init__(self):
        self.redis = redis

    def set(self, key: str, value: any, ttl: int = 300) -> None:
        self.redis.set(key, json.dumps(value), ex=ttl)

    def get(self, key: str):
        val = self.redis.get(key)
        return json.loads(val) if val else None

    def delete(self, key: str) -> None:
        self.redis.delete(key)
