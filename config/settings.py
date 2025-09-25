from dotenv import load_dotenv
import os

load_dotenv()

# LLM provider selection
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")  # default: anthropic

# Model names and API keys
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

ANTHROPIC_MODEL = "claude-opus-4-1-20250805"
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

# Redis credentials
REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

# Flag to enable/disable document-based RAG
USE_DOCUMENTS = False
