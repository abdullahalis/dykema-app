from dotenv import load_dotenv
import os
from supabase import create_client
from upstash_redis import Redis
import logging

load_dotenv()

# Set up
LLM_PROVIDER = "anthropic"  # Options: "openai", "anthropic"

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

ANTRHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-opus-4-1-20250805"

supabase = create_client(os.getenv("SUPABASE_PROJECT_URL"), os.getenv("SUPABASE_API_KEY"))

redis = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

# Configure logging 
logging.basicConfig(
    filename="app_errors.log",
    level=logging.ERROR,         # log only ERROR and above
    format="%(asctime)s - %(levelname)s - %(message)s"
)
