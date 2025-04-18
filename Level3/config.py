from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Lightweight model