import json
from storage.cache.base_cache import CacheManager
from config.services import redis
from typing import Any, Optional

class RedisCacheManager(CacheManager):
    """Redis-based implementation of CacheManager."""
    def __init__(self):
        self.redis = redis

    def set(self, key: str, value: any, ttl: int = 300) -> None:
        """Set a value in the cache with an optional Time To Live in seconds."""
        self.redis.set(key, json.dumps(value), ex=ttl)

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache by key. Returns None if not found or expired."""
        val = self.redis.get(key)
        return json.loads(val) if val else None

    def delete(self, key: str) -> None:
        """Delete a value from the cache by key."""
        self.redis.delete(key)
