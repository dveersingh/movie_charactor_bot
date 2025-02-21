from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

# Handle special characters in password
db_password = quote_plus(os.getenv("DB_PASSWORD"))

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": db_password,
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
REDIS_URL = os.getenv("REDIS_URL")