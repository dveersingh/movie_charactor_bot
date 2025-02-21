from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

# Handle special characters in password
#db_password = quote_plus(os.getenv("DB_PASSWORD"))

DB_URL= os.getenv(f"PG_URL")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
REDIS_URL = os.getenv("REDIS_URL")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_URL = os.getenv("HF_URL")