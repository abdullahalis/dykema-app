import pytest
import time
from auth.supabase_auth import SupabaseAuthManager
from storage.backend.supabase_backend import SupabaseBackend
from storage.cache.redis_cache import RedisCacheManager
from storage.combined_storage import CombinedStorageManager

USER_EMAIL = "abdullahalisye@gmail.com"
USER_PASSWORD = "password"

@pytest.fixture(scope="module")
def auth_manager():
    auth = SupabaseAuthManager()
    auth.sign_in(USER_EMAIL, USER_PASSWORD)
    yield auth
    auth.sign_out()

@pytest.fixture(scope="module")
def supabase_backend():
    return SupabaseBackend()

@pytest.fixture(scope="module")
def combined_backend():
    supabase = SupabaseBackend()
    redis_cache = RedisCacheManager()
    return CombinedStorageManager(supabase, redis_cache)

@pytest.fixture(scope="module")
def test_data(auth_manager, supabase_backend):
    """Create a conversation for the authorized user."""
    user_id = auth_manager.get_user_id()
    messages = [{"role": "user", "content": "Hello"}]
    convo_id = supabase_backend.save_conversation(user_id, None, messages)
    return user_id, convo_id

def measure_fetch_time(storage, user_id, convo_id, repeat=50):
    start = time.perf_counter()
    for _ in range(repeat):
        storage.get_messages(user_id, convo_id)
    end = time.perf_counter()
    avg_time_ms = (end - start) / repeat * 1000
    return avg_time_ms

def test_cache_vs_supabase_performance(supabase_backend, combined_backend, test_data):
    user_id, convo_id = test_data

    supabase_time = measure_fetch_time(supabase_backend, user_id, convo_id)
    combined_time = measure_fetch_time(combined_backend, user_id, convo_id)

    print(f"\nAvg fetch time (Supabase only): {supabase_time:.2f} ms")
    print(f"Avg fetch time (Supabase + Redis cache): {combined_time:.2f} ms")

    # Cached backend should be faster
    assert combined_time < supabase_time
