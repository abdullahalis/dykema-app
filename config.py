from dotenv import load_dotenv
import os
load_dotenv()

LLM_PROVIDER = "anthropic"  # Options: "openai", "anthropic", "mistral"

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

ANTRHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-opus-4-1-20250805"

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")