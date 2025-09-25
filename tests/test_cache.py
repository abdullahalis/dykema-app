import pytest
import time
from storage.cache.redis_cache import RedisCacheManager

@pytest.fixture
def cache_manager():
    return RedisCacheManager()

@pytest.fixture
def test_data():
    return "test_key", {"data": "test_value"}

def test_set_and_get_cache(cache_manager, test_data):
    key, value = test_data
    cache_manager.set(key, value, ttl=10)
    retrieved_value = cache_manager.get(key)
    assert retrieved_value == value

def test_cache_expiry(cache_manager, test_data):
    key, value = test_data
    cache_manager.set(key, value, ttl=1)
    time.sleep(2)  # Wait for the cache to expire
    retrieved_value = cache_manager.get(key)
    assert retrieved_value is None

def test_delete_cache(cache_manager, test_data):
    key, value = test_data
    cache_manager.set(key, value, ttl=10)
    cache_manager.delete(key)
    retrieved_value = cache_manager.get(key)
    assert retrieved_value is None
