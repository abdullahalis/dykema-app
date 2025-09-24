# config/services.py
import logging
from supabase import create_client
from upstash_redis import Redis
from llm.rag.pdf_loader import load_pdfs_from_folder
from llm.rag.vector_manager import VectorManager
from config import settings
import os

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
    log_dir = os.path.join(os.path.dirname(__file__), "..", "error")
    os.makedirs(log_dir, exist_ok=True)  # make sure folder exists

    log_file = os.path.join(log_dir, "app_errors.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,  # log only ERROR and above
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Optionally setup RAG components
if settings.USE_DOCUMENTS:
    print("loading pdf")
    # Load and index PDFs
    pdf_text = load_pdfs_from_folder("documents/")
    print(f"Loaded {len(pdf_text)} documents")
    vector_manager = VectorManager()
    vector_manager.add_documents(pdf_text)
    print("Vector store ready")
else:
    vector_manager = None