import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv()

# =========================
# BASE PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_PDF_DIR = DATA_DIR / "raw_pdfs"
PARSED_JSON_DIR = DATA_DIR / "parsed_json"
FAISS_INDEX_DIR = DATA_DIR / "faiss_indexes"

# =========================
# OPENAI CONFIG
# =========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LLM_MODEL = "gpt-5.2"
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 1024

# =========================
# EMBEDDINGS
# =========================
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# =========================
# RETRIEVAL
# =========================
TOP_K = 5
SIMILARITY_THRESHOLD = 0.3

# =========================
# CHUNKING
# =========================
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# =========================
# OCR
# =========================
OCR_LANGUAGE = "eng"

# =========================
# LOGGING
# =========================
LOG_LEVEL = "INFO"
