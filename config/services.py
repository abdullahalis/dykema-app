# config/services.py
import logging
from supabase import create_client
from upstash_redis import Redis
from config import settings

# Supabase client
supabase = create_client(
    settings.SUPABASE_URL, 
    settings.SUPABASE_KEY
)

# Redis client
redis = Redis(
    url=settings.REDIS_URL,
    token=settings.REDIS_TOKEN
)

# Logging setup
def setup_logging() -> None:
    logging.basicConfig(
        filename="app_errors.log",
        level=logging.ERROR,  # log only ERROR and above
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
